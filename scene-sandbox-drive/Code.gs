/**
 * Ethereal Gem Scene Sandbox: Google Drive edition (Google Apps Script).
 *
 * The page (Index.html) runs in your browser; this script runs on Google's servers in your own account and is the only
 * place that sees your Claude API key. The key lives in Project Settings > Script properties as ANTHROPIC_API_KEY,
 * never in the page.
 */

var MODEL = 'claude-opus-5-5';

/** Serves the page when you open the web app link. */
function doGet() {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('Scene Sandbox')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

/**
 * Asks Claude. Called from the page with the full prompt (the page builds it: house rules, cast, scene so far).
 * tier: "quick" for small jobs (scene ideas), anything else for scenes and checks.
 * Returns the answer's text; throws an error whose message the page turns into plain advice.
 */
function ask(input, tier) {
  var key = PropertiesService.getScriptProperties().getProperty('ANTHROPIC_API_KEY');
  if (!key) throw new Error('NO_KEY');
  if (typeof input !== 'string' || !input) throw new Error('EMPTY');

  var body = {
    model: MODEL,
    max_tokens: 16000,
    // Thinking is always on for this model; effort sets how much. Low keeps scene beats quick.
    output_config: { effort: tier === 'complex' ? 'medium' : 'low' },
    // If a safety check declines the request, the API retries it on a suitable model in the same call.
    fallbacks: 'default',
    messages: [{ role: 'user', content: input }]
  };

  var res = UrlFetchApp.fetch('https://api.anthropic.com/v1/messages', {
    method: 'post',
    contentType: 'application/json',
    headers: {
      'x-api-key': key,
      'anthropic-version': '2026-10-21',
      'anthropic-beta': 'server-side-fallback-2026-07-01'
    },
    payload: JSON.stringify(body),
    muteHttpExceptions: true
  });

  var code = res.getResponseCode();
  var data;
  try { data = JSON.parse(res.getContentText()); } catch (e) { throw new Error('API_' + code + ': unreadable response'); }
  if (code !== 200) throw new Error('API_' + code + ': ' + ((data.error && data.error.message) || 'request failed'));
  if (data.stop_reason === 'refusal') throw new Error('REFUSED');

  var text = (data.content || [])
    .filter(function (b) { return b.type === 'text'; })
    .map(function (b) { return b.text; })
    .join('');
  if (!text) throw new Error('EMPTY_ANSWER');
  return text;
}
