import { _decorator, Component, find, screen, UITransform } from 'cc';

const { ccclass, executionOrder } = _decorator;

type Profile = 'PORTRAIT' | 'LANDSCAPE';

interface Metrics {
  width: number;
  height: number;
  pxPerUnit: number;
  profile: Profile;
  marginX: number;
  marginY: number;
  gap: number;
  titleFont: number;
  bodyFont: number;
  navFont: number;
  metaFont: number;
  navHeight: number;
  actionHeight: number;
  actionWidth: number;
  navY: number;
  returnY: number;
  returnHeight: number;
  footerTop: number;
  titleY: number;
  titleHeight: number;
  observationY: number;
  observationHeight: number;
  contentTop: number;
}

@ccclass('C04WS07AResponsiveVisualLayoutCorrection')
@executionOrder(100)
export class ResponsiveVisualLayoutCorrection extends Component {
  protected lateUpdate(): void {
    const metrics = this.computeMetrics();
    if (!metrics) return;
    this.correctSharedBounds(metrics);
    this.correctResponsiveVisibility(metrics);
    this.correctLandscapeReveal(metrics);
  }

  private correctSharedBounds(m: Metrics): void {
    const navPaths = ['PrototypeNav/NavS0', 'PrototypeNav/NavS1', 'PrototypeNav/NavS2', 'PrototypeNav/NavRoute', 'PrototypeNav/NavBook'];
    const navWidth = (m.width - (2 * m.marginX) - (4 * m.gap)) / 5;
    navPaths.forEach((path, index) => {
      const x = -m.width / 2 + m.marginX + navWidth / 2 + index * (navWidth + m.gap);
      this.place(path, x, m.navY, navWidth, m.navHeight);
      this.size(`${path}/Text`, navWidth, m.navHeight);
    });

    this.place('ReturnGuard/Label', 0, m.returnY, m.width - 2 * m.marginX, m.returnHeight);
    this.place('ReadingOverlay/PageTitle', 0, m.titleY, m.width - 2 * m.marginX, m.titleHeight);
    this.place('ReadingOverlay/Observation', 0, m.observationY, m.width - 2 * m.marginX, m.observationHeight);

    const actionY = m.footerTop + m.gap + m.actionHeight / 2;
    this.place('ReadingOverlay/RecordButton', m.width / 2 - m.marginX - m.actionWidth / 2, actionY, m.actionWidth, m.actionHeight);
    this.size('ReadingOverlay/RecordButton/Text', m.actionWidth, m.actionHeight);
    this.place('ReadingOverlay/RevealButton', m.width / 2 - m.marginX - (m.actionWidth * 1.5) - m.gap, actionY, m.actionWidth, m.actionHeight);
    this.size('ReadingOverlay/RevealButton/Text', m.actionWidth, m.actionHeight);

    const wide = m.width - 2 * m.marginX;
    this.place('Route/Title', 0, m.titleY, wide, m.titleHeight);
    this.place('Route/Priority', 0, m.observationY, wide, m.observationHeight);
    this.place('MyBook/Title', 0, m.titleY, wide, m.titleHeight);
    this.place('MyBook/BookSummary', 0, m.observationY, wide, Math.max(m.observationHeight, m.bodyFont * 3));
  }

  private correctResponsiveVisibility(m: Metrics): void {
    const s0 = find('S0_OneLineSky', this.node);
    const s1 = find('S1_RedRockMouth', this.node);
    const s2 = find('S2_RiverValley', this.node);
    const reveal = find('S2_RiverValley/RevealRoot', this.node);
    const readingOverlay = find('ReadingOverlay', this.node);
    const s2Hint = find('S2_RiverValley/ScreenHint', this.node);
    const pageActive = Boolean(s0?.activeInHierarchy || s1?.activeInHierarchy || s2?.activeInHierarchy);
    const revealOpen = Boolean(reveal?.activeInHierarchy);
    const landscapeReveal = revealOpen && m.profile === 'LANDSCAPE';

    if (readingOverlay) readingOverlay.active = pageActive && !landscapeReveal;
    if (s2Hint) s2Hint.active = !revealOpen;
  }

  private correctLandscapeReveal(m: Metrics): void {
    const reveal = find('S2_RiverValley/RevealRoot', this.node);
    if (!reveal?.activeInHierarchy || m.profile !== 'LANDSCAPE') return;

    const panelTop = m.height / 2 - m.marginY;
    const evidenceHeight = Math.max(m.metaFont * 2.2, 30);
    const closeY = m.footerTop + m.gap + m.actionHeight / 2;
    const panelBottom = closeY + m.actionHeight / 2 + m.gap;
    const evidenceY = panelTop - evidenceHeight / 2;
    const claimTop = evidenceY - evidenceHeight / 2 - m.gap;
    const claimHeight = Math.max(56, claimTop - panelBottom);
    const claimWidth = (m.width - 2 * m.marginX - 2 * m.gap) / 3;

    this.place('S2_RiverValley/RevealRoot/EvidenceStatus', 0, evidenceY, m.width - 2 * m.marginX, evidenceHeight);
    const claims = [
      'S2_RiverValley/RevealRoot/Fact',
      'S2_RiverValley/RevealRoot/Narrative',
      'S2_RiverValley/RevealRoot/DesignReading',
    ];
    claims.forEach((path, index) => {
      const x = -m.width / 2 + m.marginX + claimWidth / 2 + index * (claimWidth + m.gap);
      this.place(path, x, panelBottom + claimHeight / 2, claimWidth, claimHeight);
    });
    this.place('S2_RiverValley/RevealRoot/CloseReveal', m.width / 2 - m.marginX - m.actionWidth / 2, closeY, m.actionWidth, m.actionHeight);
    this.size('S2_RiverValley/RevealRoot/CloseReveal/Text', m.actionWidth, m.actionHeight);
  }

  private computeMetrics(): Metrics | null {
    const canvas = this.node.getComponent(UITransform);
    if (!canvas) return null;
    const width = canvas.contentSize.width;
    const height = canvas.contentSize.height;
    if (width <= 0 || height <= 0) return null;
    const pxPerUnit = Math.max(0.1, screen.windowSize.width / width);
    const profile: Profile = height < width * 0.8 ? 'LANDSCAPE' : 'PORTRAIT';
    const unit = (px: number, min: number, max: number): number => this.clamp(px / pxPerUnit, min, max);
    const marginX = unit(24, 28, 64);
    const marginY = profile === 'LANDSCAPE' ? unit(16, 16, 34) : unit(28, 28, 72);
    const gap = unit(10, 10, 26);
    const titleFont = unit(28, 30, 64);
    const bodyFont = unit(17, 18, 42);
    const navFont = unit(14, 16, 36);
    const metaFont = unit(14, 14, 34);
    const navHeight = unit(48, 52, 112);
    const actionHeight = navHeight;
    const actionWidth = unit(132, 160, 300);
    const bottom = -height / 2 + marginY;
    const navY = bottom + navHeight / 2;
    const returnHeight = Math.max(metaFont * 2.2, unit(34, 36, 82));
    const returnY = bottom + navHeight + gap + returnHeight / 2;
    const footerTop = bottom + navHeight + gap + returnHeight + gap;
    const titleHeight = Math.max(titleFont * 1.45, unit(46, 50, 108));
    const observationHeight = profile === 'LANDSCAPE' ? Math.max(bodyFont * 2.2, 48) : Math.max(bodyFont * 3, 72);
    const titleY = height / 2 - marginY - titleHeight / 2;
    const observationY = titleY - titleHeight / 2 - gap - observationHeight / 2;
    const contentTop = observationY - observationHeight / 2 - gap;
    return {
      width, height, pxPerUnit, profile, marginX, marginY, gap, titleFont, bodyFont, navFont, metaFont,
      navHeight, actionHeight, actionWidth, navY, returnY, returnHeight, footerTop,
      titleY, titleHeight, observationY, observationHeight, contentTop,
    };
  }

  private place(path: string, x: number, y: number, width: number, height: number): void {
    const node = find(path, this.node);
    if (!node) return;
    this.size(path, width, height);
    node.setPosition(x, y, 0);
  }

  private size(path: string, width: number, height: number): void {
    const node = find(path, this.node);
    if (!node) return;
    const transform = node.getComponent(UITransform) ?? node.addComponent(UITransform);
    transform.setContentSize(Math.max(1, width), Math.max(1, height));
  }

  private clamp(value: number, min: number, max: number): number {
    return Math.min(max, Math.max(min, value));
  }
}
