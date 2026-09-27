import { spawnSync } from 'node:child_process'

const candidates = process.platform === 'win32'
  ? [
      ['py', ['-3']],
      ['python', []],
      ['python3', []],
    ]
  : [
      ['python3', []],
      ['python', []],
    ]

let selected = null
for (const [command, prefix] of candidates) {
  const probe = spawnSync(command, [...prefix, '--version'], { encoding: 'utf8' })
  if (probe.status === 0) {
    selected = [command, prefix]
    break
  }
}

if (!selected) {
  console.error('No usable Python interpreter found for Design System host tests.')
  process.exit(1)
}

const [command, prefix] = selected
const args = [
  ...prefix,
  '-m', 'unittest',
  '00-governance.tests.test_design_system_local_host_v01',
  '00-governance.tests.test_host_runtime_contract_v01',
  '00-governance.tests.test_host_runtime_probe_v01',
  '00-governance.tests.test_project_repository_migration_v01',
  '-v',
]
const result = spawnSync(command, args, { stdio: 'inherit' })
process.exit(result.status ?? 1)
