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
    client = new Client({ name: 'oleander-ws07a-materializer', version: '0.3.0' }, { capabilities: { tools: {} } });
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

async function addComponent(nodePath, component, label) {
  return assertOk(await callTool('scene-add-component', {
    addComponentInfo: { nodePath, component },
  }), label);
}

async function createContractNode(spec) {
  assertOk(await callTool('scene-create-node-by-type', {
    options: {
      path: spec.path,
      name: spec.path.split('/').at(-1),
      nodeType: 'Empty',
      workMode: '2d',
    },
  }), `create ${spec.path}`);

  if (spec.type === 'Label') {
    const added = await addComponent(spec.path, 'cc.Label', `add Label ${spec.path}`);
    const componentPath = added?.path;
    if (!componentPath) throw new Error(`add Label ${spec.path}: component path missing`);
    const properties = { string: spec.label ?? '' };
    if (Number.isFinite(spec.fontSize)) {
      properties.fontSize = spec.fontSize;
      properties.lineHeight = Math.max(spec.fontSize + 4, Math.round(spec.fontSize * 1.2));
    }
    assertOk(await callTool('scene-set-component-property', {
      setPropertyOptions: { componentPath, properties },
    }), `set Label ${spec.path}`);
  } else if (spec.type === 'Button') {
    await addComponent(spec.path, 'cc.Button', `add Button ${spec.path}`);
  }

  if (typeof spec.active === 'boolean') {
    assertOk(await callTool('scene-update-node', {
      options: { path: spec.path, properties: { active: spec.active } },
    }), `set active ${spec.path}`);
  }
}

function managedRoots() {
  return [...new Set(contract.nodes.map((spec) => spec.path.split('/').slice(0, 2).join('/')))].filter((pathValue) => pathValue.startsWith('Canvas/'));
}

function componentContracts() {
  return [contract.controller, ...(Array.isArray(contract.corrections) ? contract.corrections : [])];
}

async function componentAttached(spec) {
  const host = assertOk(await callTool('scene-query-node', {
    options: { path: spec.nodePath, includeChildren: false, includeComponents: true },
  }), `query component host ${spec.nodePath}`);
  return (host.components ?? []).some((item) => {
    const text = `${item.type ?? ''} ${item.path ?? ''} ${item.value ?? ''}`;
    return text.includes(spec.className) || text.includes(path.basename(spec.component, '.ts'));
  });
}

await connect();
try {
  const toolList = await client.listTools({}, { timeout: 30000 });
  const available = new Set(toolList.tools.map((tool) => tool.name));
  const required = [
    'scene-create', 'scene-open', 'scene-save', 'scene-reload', 'scene-close',
    'scene-query-node', 'scene-create-node-by-type', 'scene-update-node', 'scene-delete-node',
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

  for (const rootPath of managedRoots()) {
    const existing = await callTool('scene-query-node', { options: { path: rootPath, includeChildren: false, includeComponents: true } });
    if (existing.code === 200) {
      assertOk(await callTool('scene-delete-node', { options: { path: rootPath } }), `delete stale managed root ${rootPath}`);
    }
  }

  for (const spec of contract.nodes) await createContractNode(spec);

  const mountedComponents = [];
  for (const spec of componentContracts()) {
    let componentPath = 'existing';
    if (!await componentAttached(spec)) {
      const added = await addComponent(spec.nodePath, spec.component, `mount ${spec.className}`);
      componentPath = added?.path;
      if (!componentPath) throw new Error(`mount ${spec.className}: component path missing`);
    }
    mountedComponents.push({ className: spec.className, componentPath, gate: spec.gate ?? 'BASE' });
  }

  assertOk(await callTool('scene-save', {}), 'save VisualPrototype.scene');
  assertOk(await callTool('scene-reload', {}), 'reload VisualPrototype.scene');

  for (const spec of contract.nodes) {
    assertOk(await callTool('scene-query-node', { options: { path: spec.path, includeChildren: false, includeComponents: true } }), `verify ${spec.path}`);
  }
  for (const spec of componentContracts()) {
    if (!await componentAttached(spec)) throw new Error(`verify mounted component failed: ${spec.className}`);
  }

  assertOk(await callTool('scene-save', {}), 'final save VisualPrototype.scene');
  await callTool('scene-close', {});

  const proof = {
    gate: 'OFFICIAL_MCP_SCENE_MATERIALIZATION_PASS',
    sceneUrl,
    contractVersion: contract.version,
    nodeCount: contract.nodes.length,
    managedRootCount: managedRoots().length,
    controller: contract.controller.className,
    corrections: (contract.corrections ?? []).map((item) => item.className),
    mountedComponents,
    defaultTemplateVisuals: 'REMOVED_BY_EMPTY_NODE_MATERIALIZATION',
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
