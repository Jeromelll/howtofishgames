// www.howtofishgames.com -> howtofishgames.com（301，保留路径和查询串）
export async function onRequest({ request, next }) {
  const url = new URL(request.url);
  if (url.hostname === "www.howtofishgames.com") {
    url.hostname = "howtofishgames.com";
    return Response.redirect(url.toString(), 301);
  }
  return next();
}
