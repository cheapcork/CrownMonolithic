# from channels.auth import AuthMiddleware
# from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import AnonymousUser
# from channels.sessions import CookieMiddleware, SessionMiddleware
# from channels.db import database_sync_to_async
# from django.contrib.auth import get_user_model
#
# @database_sync_to_async
# def get_user(token=0):
#     try:
#         return Token.objects.get(key=token).user
#     except get_user_model().DoesNotExist:
#         return AnonymousUser
#
#
# class TokenAuthMiddleware:
#     def __init__(self, instance):
#         self.instance = instance
#
#     async def __call__(self, scope, receive, send):
#         if 'Authorization' in dict(scope['cookies']):
#             token_name, token_key = scope['cookies']['Authorization'].split('%20')
#             scope['user'] = await get_user(token_key)
#         return await self.instance(scope, receive, send)
#
#
# def TokenAuthMiddlewareStack(inner):
#     return CookieMiddleware(
#         TokenAuthMiddleware(
#             SessionMiddleware(
#                 AuthMiddleware(
#                     inner
#                 )
#             )
#         )
#     )
#
