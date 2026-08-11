export type PhoneState = 'S0' | 'S1' | 'S2' | 'S3';
export type AppRoute = 'TODAY' | 'ROUTE' | 'NODE' | 'BOOK' | 'SERVICE' | 'CLOSURE';

export interface ReadingProgress {
  currentNodeId: number;
  readNodeIds: number[];
  currentChapter: string;
  route: AppRoute;
  phoneState: PhoneState;
}

export const initialProgress: ReadingProgress = {
  currentNodeId: 1,
  readNodeIds: [],
  currentChapter: 'CH01',
  route: 'TODAY',
  phoneState: 'S1'
};

export function recordNode(state: ReadingProgress, nodeId: number): ReadingProgress {
  const next = state.readNodeIds.includes(nodeId) ? state.readNodeIds : [...state.readNodeIds, nodeId];
  return { ...state, readNodeIds: next };
}
