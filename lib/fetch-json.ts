export async function fetchJson(url: string, options: RequestInit = {}, timeout = 100000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout);
  const abort = () => controller.abort();
  options.signal?.addEventListener('abort', abort, { once: true });
  if (options.signal?.aborted) controller.abort();
  try {
    const response = await fetch(url, { ...options, signal: controller.signal });
    const data = await response.json().catch(() => { throw new Error('The server returned an unreadable response. Please try again.'); });
    if (!response.ok) throw new Error(data.error || 'Something went wrong. Please try again.');
    return data;
  } catch (error) {
    if (controller.signal.aborted) throw new Error('This is taking longer than expected. Please try a smaller set or try again.');
    throw error;
  } finally {
    clearTimeout(timer);
    options.signal?.removeEventListener('abort', abort);
  }
}
