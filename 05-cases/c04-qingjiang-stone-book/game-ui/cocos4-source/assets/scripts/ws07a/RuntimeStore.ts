import type { ReadingPage, RuntimeBundle, PrototypeScreenId } from './RuntimeTypes';

export interface RuntimeState { currentScreen: PrototypeScreenId; currentPageId?: string; recordedPageIds: string[]; revealOpen: boolean; }

class Store {
  private bundle: RuntimeBundle | null = null;
  private state: RuntimeState = { currentScreen: 'S0_ONE_LINE_SKY', recordedPageIds: [], revealOpen: false };
  public hydrate(bundle: RuntimeBundle): void { this.bundle = bundle; }
  public get snapshot(): Readonly<RuntimeState> { return this.state; }
  public get manifest() { return this.bundle?.manifest ?? null; }
  public setScreen(screen: PrototypeScreenId): void { this.state.currentScreen = screen; this.state.revealOpen = false; }
  public setCurrentPage(pageId?: string): void { this.state.currentPageId = pageId; }
  public getPage(pageId: string): ReadingPage | undefined {
    const manifest = this.bundle?.manifest;
    if (!manifest) return undefined;
    return [...manifest.corePages, ...manifest.companionPages].find((page) => page.id === pageId);
  }
  public record(pageId: string): void { if (!this.state.recordedPageIds.includes(pageId)) this.state.recordedPageIds.push(pageId); }
  public setReveal(open: boolean): void { this.state.revealOpen = open; }
  public getRecordedPages(): ReadingPage[] { return this.state.recordedPageIds.map((id) => this.getPage(id)).filter((page): page is ReadingPage => Boolean(page)); }
}

export const RuntimeStore = new Store();
