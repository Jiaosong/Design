import { JsonAsset, resources } from 'cc';
import type { RuntimeBundle, RuntimeManifest, UiTokens } from './RuntimeTypes';

const MANIFEST_PATH = 'c04/ws07a/runtime-manifest';
const TOKENS_PATH = 'c04/ws07a/ui-tokens';

function loadJson<T>(path: string): Promise<T> {
  return new Promise<T>((resolve, reject) => {
    resources.load(path, JsonAsset, (err, asset) => {
      if (err) { reject(err); return; }
      if (!asset?.json) { reject(new Error(`JSON asset has no payload: ${path}`)); return; }
      resolve(asset.json as T);
    });
  });
}

export class RuntimeCatalog {
  public static async load(): Promise<RuntimeBundle> {
    const [manifest, tokens] = await Promise.all([
      loadJson<RuntimeManifest>(MANIFEST_PATH),
      loadJson<UiTokens>(TOKENS_PATH),
    ]);
    return { manifest, tokens };
  }
}
