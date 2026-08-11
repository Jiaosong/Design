export const GAME_UI_RULES = {
  topLevelIA: ['今日', '路线', '我的石书', '服务'],
  primaryActions: ['继续行走', '记录此页', '揭示这一层', '生成本次石书'],
  stampTypes: ['AUTO', 'OBSERVATION', 'REVEAL', 'PHYSICAL'],
  noRewardEconomy: true,
  allowIncompleteBook: true,
  fieldNotVerified: ['GPS', 'routeTime', 'networkQuality', 'ARSuccessRate', 'PHY01Engineering', 'safety', 'maintenance']
} as const;
