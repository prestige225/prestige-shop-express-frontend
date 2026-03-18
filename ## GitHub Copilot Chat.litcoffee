## GitHub Copilot Chat

- Extension: 0.39.2 (prod)
- VS Code: 1.111.0 (ce099c1ed25d9eb3076c11e4a280f3eb52b4fbeb)
- OS: win32 10.0.19045 x64
- GitHub Account: princesserachel37-sketch

## Network

User Settings:
```json
  "http.systemCertificatesNode": true,
  "github.copilot.advanced.debug.useElectronFetcher": true,
  "github.copilot.advanced.debug.useNodeFetcher": false,
  "github.copilot.advanced.debug.useNodeFetchFetcher": true
```

Connecting to https://api.github.com:
- DNS ipv4 Lookup: 140.82.121.6 (12 ms)
- DNS ipv6 Lookup: Error (28 ms): getaddrinfo ENOTFOUND api.github.com
- Proxy URL: None (2 ms)
- Electron fetch (configured): Error (1245 ms): Error: net::ERR_CERT_DATE_INVALID
	at SimpleURLLoaderWrapper.<anonymous> (node:electron/js2c/utility_init:2:10684)
	at SimpleURLLoaderWrapper.emit (node:events:519:28)
  [object Object]
  {"is_request_error":true,"network_process_crashed":false}
- Node.js https: Error (248 ms): Error: certificate has expired
	at TLSSocket.onConnectSecure (node:_tls_wrap:1697:34)
	at TLSSocket.emit (node:events:519:28)
	at TLSSocket._finishInit (node:_tls_wrap:1095:8)
	at ssl.onhandshakedone (node:_tls_wrap:881:12)
- Node.js fetch: Error (274 ms): TypeError: fetch failed
	at node:internal/deps/undici/undici:14902:13
	at process.processTicksAndRejections (node:internal/process/task_queues:105:5)
	at async n._fetch (c:\Users\RCK COMPUTERS\.vscode\extensions\github.copilot-chat-0.39.2\dist\extension.js:5075:5229)
	at async n.fetch (c:\Users\RCK COMPUTERS\.vscode\extensions\github.copilot-chat-0.39.2\dist\extension.js:5075:4541)
	at async u (c:\Users\RCK COMPUTERS\.vscode\extensions\github.copilot-chat-0.39.2\dist\extension.js:5107:186)
	at async Zm._executeContributedCommand (file:///c:/Users/RCK%20COMPUTERS/AppData/Local/Programs/Microsoft%20VS%20Code/ce099c1ed2/resources/app/out/vs/workbench/api/node/extensionHostProcess.js:494:48675)
  Error: certificate has expired
  	at TLSSocket.onConnectSecure (node:_tls_wrap:1697:34)
  	at TLSSocket.emit (node:events:519:28)
  	at TLSSocket._finishInit (node:_tls_wrap:1095:8)
  	at ssl.onhandshakedone (node:_tls_wrap:881:12)

Connecting to https://api.githubcopilot.com/_ping:
- DNS ipv4 Lookup: 140.82.113.22 (39 ms)
- DNS ipv6 Lookup: Error (238 ms): getaddrinfo ENOTFOUND api.githubcopilot.com
- Proxy URL: None (3 ms)
- Electron fetch (configured): Error (396 ms): Error: net::ERR_CERT_DATE_INVALID
	at SimpleURLLoaderWrapper.<anonymous> (node:electron/js2c/utility_init:2:10684)
	at SimpleURLLoaderWrapper.emit (node:events:519:28)
  [object Object]
  {"is_request_error":true,"network_process_crashed":false}
- Node.js https: Error (393 ms): Error: certificate has expired
	at TLSSocket.onConnectSecure (node:_tls_wrap:1697:34)
	at TLSSocket.emit (node:events:519:28)
	at TLSSocket._finishInit (node:_tls_wrap:1095:8)
	at ssl.onhandshakedone (node:_tls_wrap:881:12)
- Node.js fetch: Error (418 ms): TypeError: fetch failed
	at node:internal/deps/undici/undici:14902:13
	at process.processTicksAndRejections (node:internal/process/task_queues:105:5)
	at async n._fetch (c:\Users\RCK COMPUTERS\.vscode\extensions\github.copilot-chat-0.39.2\dist\extension.js:5075:5229)
	at async n.fetch (c:\Users\RCK COMPUTERS\.vscode\extensions\github.copilot-chat-0.39.2\dist\extension.js:5075:4541)
	at async u (c:\Users\RCK COMPUTERS\.vscode\extensions\github.copilot-chat-0.39.2\dist\extension.js:5107:186)
	at async Zm._executeContributedCommand (file:///c:/Users/RCK%20COMPUTERS/AppData/Local/Programs/Microsoft%20VS%20Code/ce099c1ed2/resources/app/out/vs/workbench/api/node/extensionHostProcess.js:494:48675)
  Error: certificate has expired
  	at TLSSocket.onConnectSecure (node:_tls_wrap:1697:34)
  	at TLSSocket.emit (node:events:519:28)
  	at TLSSocket._finishInit (node:_tls_wrap:1095:8)
  	at ssl.onhandshakedone (node:_tls_wrap:881:12)

Connecting to https://copilot-proxy.githubusercontent.com/_ping:
- DNS ipv4 Lookup: 20.199.39.224 (38 ms)
- DNS ipv6 Lookup: Error (43 ms): getaddrinfo ENOTFOUND copilot-proxy.githubusercontent.com
- Proxy URL: None (3 ms)
- Electron fetch (configured): Error (520 ms): Error: net::ERR_CERT_DATE_INVALID
	at SimpleURLLoaderWrapper.<anonymous> (node:electron/js2c/utility_init:2:10684)
	at SimpleURLLoaderWrapper.emit (node:events:519:28)
  [object Object]
  {"is_request_error":true,"network_process_crashed":false}
- Node.js https: Error (271 ms): Error: certificate has expired
	at TLSSocket.onConnectSecure (node:_tls_wrap:1697:34)
	at TLSSocket.emit (node:events:519:28)
	at TLSSocket._finishInit (node:_tls_wrap:1095:8)
	at ssl.onhandshakedone (node:_tls_wrap:881:12)
- Node.js fetch: Error (314 ms): TypeError: fetch failed
	at node:internal/deps/undici/undici:14902:13
	at process.processTicksAndRejections (node:internal/process/task_queues:105:5)
	at async n._fetch (c:\Users\RCK COMPUTERS\.vscode\extensions\github.copilot-chat-0.39.2\dist\extension.js:5075:5229)
	at async n.fetch (c:\Users\RCK COMPUTERS\.vscode\extensions\github.copilot-chat-0.39.2\dist\extension.js:5075:4541)
	at async u (c:\Users\RCK COMPUTERS\.vscode\extensions\github.copilot-chat-0.39.2\dist\extension.js:5107:186)
	at async Zm._executeContributedCommand (file:///c:/Users/RCK%20COMPUTERS/AppData/Local/Programs/Microsoft%20VS%20Code/ce099c1ed2/resources/app/out/vs/workbench/api/node/extensionHostProcess.js:494:48675)
  Error: certificate has expired
  	at TLSSocket.onConnectSecure (node:_tls_wrap:1697:34)
  	at TLSSocket.emit (node:events:519:28)
  	at TLSSocket._finishInit (node:_tls_wrap:1095:8)
  	at ssl.onhandshakedone (node:_tls_wrap:881:12)

Connecting to https://mobile.events.data.microsoft.com: Error (1100 ms): Error: net::ERR_CERT_DATE_INVALID
	at SimpleURLLoaderWrapper.<anonymous> (node:electron/js2c/utility_init:2:10684)
	at SimpleURLLoaderWrapper.emit (node:events:519:28)
  [object Object]
  {"is_request_error":true,"network_process_crashed":false}
Connecting to https://dc.services.visualstudio.com: Error (1968 ms): Error: net::ERR_CERT_DATE_INVALID
	at SimpleURLLoaderWrapper.<anonymous> (node:electron/js2c/utility_init:2:10684)
	at SimpleURLLoaderWrapper.emit (node:events:519:28)
  [object Object]
  {"is_request_error":true,"network_process_crashed":false}
Connecting to https://copilot-telemetry.githubusercontent.com/_ping: Error (411 ms): Error: certificate has expired
	at TLSSocket.onConnectSecure (node:_tls_wrap:1697:34)
	at TLSSocket.emit (node:events:519:28)
	at TLSSocket._finishInit (node:_tls_wrap:1095:8)
	at ssl.onhandshakedone (node:_tls_wrap:881:12)
Connecting to https://copilot-telemetry.githubusercontent.com/_ping: Error (381 ms): Error: certificate has expired
	at TLSSocket.onConnectSecure (node:_tls_wrap:1697:34)
	at TLSSocket.emit (node:events:519:28)
	at TLSSocket._finishInit (node:_tls_wrap:1095:8)
	at ssl.onhandshakedone (node:_tls_wrap:881:12)
Connecting to https://default.exp-tas.com: Error (416 ms): Error: certificate has expired
	at TLSSocket.onConnectSecure (node:_tls_wrap:1697:34)
	at TLSSocket.emit (node:events:519:28)
	at TLSSocket._finishInit (node:_tls_wrap:1095:8)
	at ssl.onhandshakedone (node:_tls_wrap:881:12)

Number of system certificates: 20

## Documentation

In corporate networks: [Troubleshooting firewall settings for GitHub Copilot](https://docs.github.com/en/copilot/troubleshooting-github-copilot/troubleshooting-firewall-settings-for-github-copilot).