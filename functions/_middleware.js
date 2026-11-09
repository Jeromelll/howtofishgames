// www.howtofishgames.com -> howtofishgames.com（301，保留路径和查询串）
export async function onRequest({ request, next }) {
  const url = new URL(request.url);
  if (url.hostname === "www.howtofishgames.com") {
    url.hostname = "howtofishgames.com";
    return Response.redirect(url.toString(), 301);
  }
  const response = await next();
  // 404 模板被直连访问（200）时返回真正的 404 状态，避免软 404
  if (response.status === 200 && (url.pathname === "/404" || url.pathname === "/404.html")) {
    return new Response(response.body, { status: 404, headers: response.headers });
  }
  return response;
}
