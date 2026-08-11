#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

const projectPath = path.resolve(process.argv[2] ?? '');
const port = Number(process.argv[3] ?? process.env.OLEANDER_COCOS_MCP_PORT ?? 9527);
if (!projectPath || !fs.existsSync(projectPath)) throw new Error(`Cocos project not found: ${projectPath}`);
if (!Number.isInteger(port) || port < 1 || port > 65535) throw new Error(`Invalid MCP port: ${port}`);

const toolRoot = process.env.OLEANDER_COCOS_HOME ?? process.env.OLEANDER_COCOS_TOOL_ROOT ?? '/opt/oleander/cocos4';
const cliPackage = path.join(toolRoot, 'cli', 'package.json');
if (!fs.existsSync(cliPackage)) throw new Error(`Pinned COCOS CLI package missing: ${cliPackage}`);
const requireFromCli = createRequire(cliPackage);
const importFromCli = async (specifier) => import(pathToFileURL(requireFromCli.resolve(specifier)).href);
const { Client } = await importFromCli('@modelcontextprotocol/sdk/client/index.js');
const { StreamableHTTPClientTransport } = await importFromCli('@modelcontextprotocol/sdk/client/streamableHttp.js');

const contractPath = path.join(projectPath, 'assets/resources/c04/ws07a/scene-contract.json');
const contract = JSON.parse(fs.readFileSync(contractPath, 'utf8'));
const mcpUrl = new URL(`http://127.0.0.1:${port}/mcp`);
let client;
let transport;

async function connect() {
  let lastError;
  for (let attempt = 1; attempt <= 90; attempt += 1) {
    transport = new StreamableHTTPClientTransport(mcpUrl);
    client = new Client({ name: 'oleander-ws07a-materializer', version: '0.1.0' }, { capabilities: { tools: {} } });
    try {
      await client.connect(transport);
      return;
    } catch (error) {
      lastError = error;
      try { await client.close(); } catch {}
      try { await transport.close(); } catch {}
      client = undefined;
      transport = undefined;
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }
  }
  throw lastError instanceof Error ? lastError : new Error(String(lastError));
}

async function callTool(name, args = {}) {
  const raw = await client.callTool({ name, arguments: args }, undefined, { timeout: 60000 });
  const text = raw?.content?.find?.((item) => item.type === 'text')?.text;
  if (!text) throw new Error(`${name}: MCP response has no text payload`);
  const parsed = JSON.parse(text);
  const result = parsed?.result;
  if (!result || typeof result.code !== 'number') throw new Error(`${name}: malformed API result`);
  return result;
}

function assertOk(result, label) {
  if (result.code !== 200) throw new Error(`${label}: ${result.reason ?? `code=${result.code}`}`);
  return result.data;
}

async function ensureNode(spec) {
  const query = await callTool('scene-query-node', { options: { path: spec.path, includeChildren: false, includeComponents: true } });
  if (query.code === 200) return query.data;
  return assertOk(await callTool('scene-create-node-by-type', {
    options: {
      path: spec.path,
      name: spec.path.split('/').at(-1),
      nodeType: spec.type,
      workMode: '2d',
      ...(spec.position ? { position: spec.position } : {}),
    },
  }), `create ${spec.path}`);
}

async function setNodeActive(pathValue, active) {
  assertOk(await callTool('scene-update-node', { options: { path: pathValue, properties: { active } } }), `set active ${pathValue}`);
}

async function setLabel(spec) {
  if (typeof spec.label !== 'string') return;
  const componentPath = `${spec.path}/cc.Label`;
  let queried = await callTool('scene-query-component', { component: { componentPath } });
  if (queried.code !== 200) {
    assertOk(await callTool('scene-add-component', { addComponentInfo: { nodePath: spec.path, component: 'cc.Label' } }), `add Label ${spec.path}`);
    queried = await callTool('scene-query-component', { component: { componentPath } });
  }
  assertOk(queried, `query Label ${spec.path}`);
  const properties = { string: spec.label };
  if (Number.isFinite(spec.fontSize)) {
    properties.fontSize = spec.fontSize;
    properties.lineHeight = Math.max(spec.fontSize + 4, Math.round(spec.fontSize * 1.2));
  }
  assertOk(await callTool('scene-set-component-property', { setPropertyOptions: { componentPath, properties } }), `set Label ${spec.path}`);
}

await connect();
try {
  const toolList = await client.listTools({}, { timeout: 30000 });
  const available = new Set(toolList.tools.map((tool) => tool.name));
  const required = [
    'scene-create', 'scene-open', 'scene-save', 'scene-reload', 'scene-close',
    'scene-query-node', 'scene-create-node-by-type', 'scene-update-node',
    'scene-add-component', 'scene-query-component', 'scene-set-component-property',
  ];
  for (const name of required) if (!available.has(name)) throw new Error(`Pinned MCP tool missing: ${name}`);

  const sceneUrl = `${contract.scene.dbURL}/${contract.scene.baseName}.scene`;
  let opened = await callTool('scene-open', { options: { dbURLOrUUID: sceneUrl } });
  if (opened.code !== 200) {
    assertOk(await callTool('scene-create', { options: {
      dbURL: contract.scene.dbURL,
      baseName: contract.scene.baseName,
      templateType: contract.scene.templateType,
    } }), 'create VisualPrototype.scene');
    opened = await callTool('scene-open', { options: { dbURLOrUUID: sceneUrl } });
  }
  assertOk(opened, 'open VisualPrototype.scene');

  const canvas = await callTool('scene-query-node', { options: { path: 'Canvas', includeChildren: true, includeComponents: true } });
  if (canvas.code !== 200) {
    assertOk(await callTool('scene-create-node-by-type', { options: { path: 'Canvas', name: 'Canvas', nodeType: 'Canvas', workMode: '2d' } }), 'create Canvas');
  }

  for (const spec of contract.nodes) {
    await ensureNode(spec);
    if (typeof spec.active === 'boolean') await setNodeActive(spec.path, spec.active);
    await setLabel(spec);
  }

  const canvasAfterNodes = assertOk(await callTool('scene-query-node', { options: { path: contract.controller.nodePath, includeChildren: true, includeComponents: true } }), 'query controller host');
  const attached = (canvasAfterNodes.components ?? []).some((item) => {
    const text = `${item.type ?? ''} ${item.path ?? ''} ${item.value ?? ''}`;
    return text.includes(contract.controller.className) || text.includes('VisualPrototypeController');
  });

  let controllerPath;
  if (!attached) {
    const added = assertOk(await callTool('scene-add-component', { addComponentInfo: {
      nodePath: contract.controller.nodePath,
      component: contract.controller.component,
    } }), 'mount WS-07A controller');
    controllerPath = added?.path;
  }

  assertOk(await callTool('scene-save', {}), 'save VisualPrototype.scene');
  assertOk(await callTool('scene-reload', {}), 'reload VisualPrototype.scene');

  for (const spec of contract.nodes) {
    assertOk(await callTool('scene-query-node', { options: { path: spec.path, includeChildren: false, includeComponents: false } }), `verify ${spec.path}`);
  }
  if (controllerPath) {
    assertOk(await callTool('scene-query-component', { component: { componentPath: controllerPath } }), 'verify mounted WS-07A controller');
  }

  assertOk(await callTool('scene-save', {}), 'final save VisualPrototype.scene');
  await callTool('scene-close', {});

  const proof = {
    gate: 'OFFICIAL_MCP_SCENE_MATERIALIZATION_PASS',
    sceneUrl,
    nodeCount: contract.nodes.length,
    controller: contract.controller.className,
    controllerPath: controllerPath ?? 'existing',
  };
  const proofPath = path.join(projectPath, 'temp', 'oleander-ws07a-scene-proof.json');
  fs.mkdirSync(path.dirname(proofPath), { recursive: true });
  fs.writeFileSync(proofPath, `${JSON.stringify(proof, null, 2)}\n`);
  console.log('PASS: WS-07A VisualPrototype.scene materialized through pinned COCOS MCP');
  console.log(JSON.stringify(proof, null, 2));
} finally {
  try { await client?.close(); } catch {}
  try { await transport?.close(); } catch {}
}
