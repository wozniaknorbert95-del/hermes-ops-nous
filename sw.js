/* Akademia OS — service worker (Hermes: Web Push + notification click).
 *
 * Zakres: WYŁĄCZNIE powiadomienia. Ten SW celowo NIE cache'uje HTML —
 * handoff Fali 0-2 odnotował ryzyko serwowania nieświeżej Akademii z cache.
 *
 * Push wysyła VPS (scripts/push-send.py) kluczem VAPID, który żyje tylko na VPS.
 * Tutaj nie ma i nie będzie żadnego klucza ani sekretu.
 */

self.addEventListener('install', function () {
  self.skipWaiting();
});

self.addEventListener('activate', function (event) {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('push', function (event) {
  var payload = {
    title: 'Akademia OS',
    body: 'Jeden kawał do zrobienia — otwórz Akademię.',
    url: './DASHBOARD.html',
    tag: 'akademia-kawal'
  };
  try {
    if (event.data) {
      var incoming = event.data.json();
      if (incoming && typeof incoming === 'object') {
        payload.title = incoming.title || payload.title;
        payload.body = incoming.body || payload.body;
        payload.url = incoming.url || payload.url;
        payload.tag = incoming.tag || payload.tag;
      }
    }
  } catch (err) {
    try {
      if (event.data) payload.body = event.data.text();
    } catch (err2) {
      /* zostaje domyślny payload */
    }
  }
  event.waitUntil(
    self.registration.showNotification(payload.title, {
      body: payload.body,
      tag: payload.tag,
      lang: 'pl',
      icon: './icons/icon-192.png',
      badge: './icons/icon-192.png',
      data: { url: payload.url }
    })
  );
});

self.addEventListener('notificationclick', function (event) {
  event.notification.close();
  var target = './DASHBOARD.html';
  try {
    if (event.notification.data && event.notification.data.url) {
      target = event.notification.data.url;
    }
  } catch (err) {
    /* zostaje domyślny target */
  }
  event.waitUntil(
    self.clients
      .matchAll({ type: 'window', includeUncontrolled: true })
      .then(function (clientList) {
        for (var i = 0; i < clientList.length; i++) {
          var client = clientList[i];
          if (client.url && client.url.indexOf('DASHBOARD.html') >= 0 && 'focus' in client) {
            return client.focus();
          }
        }
        if (self.clients.openWindow) return self.clients.openWindow(target);
        return undefined;
      })
  );
});

/* Lokalny test z Akademii (bez push service) — dowód, że ścieżka powiadomienia działa.
   Odpowiada na port, więc strona wie, czy powiadomienie NAPRAWDĘ się pokazało. */
self.addEventListener('message', function (event) {
  if (!event.data || event.data.type !== 'akademia-test') return;
  var port = event.ports && event.ports[0];
  var shown = self.registration.showNotification('Akademia OS — test', {
    body: 'Powiadomienia działają. Prawdziwy push przyjdzie z VPS przy zamkniętej aplikacji.',
    tag: 'akademia-test',
    lang: 'pl',
    icon: './icons/icon-192.png'
  });
  event.waitUntil(
    shown.then(
      function () {
        if (port) port.postMessage({ ok: true });
      },
      function (err) {
        if (port) port.postMessage({ ok: false, error: String((err && err.message) || err) });
      }
    )
  );
});
