export interface QingjiangNode {
  id: number;
  name: string;
  chapter: string;
  phone: 'S0' | 'S1' | 'S2';
  stamp: string;
  action: string;
  mode: 'LANDSCAPE' | 'PROMPT' | 'REVEAL';
}

export function nodeLabel(node: QingjiangNode): string {
  return `${String(node.id).padStart(2, '0')} ${node.name}`;
}

export function shouldHideChrome(node: QingjiangNode): boolean {
  return node.phone === 'S0';
}
