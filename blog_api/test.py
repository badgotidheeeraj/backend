# import requests
# import jwt

# def validate_token(token):
#     jwks_url = "https://login.microsoftonline.com/YOUR_TENANT_ID/discovery/v2.0/keys"
#     jwks = requests.get(jwks_url).json()
#     jwks_client = jwt.PyJWKClient(jwks_url)
#     signing_key = jwks_client.get_signing_key_from_jwt(token).key

#     try:
#         decoded_token = jwt.decode(
#             token,
#             signing_key,
#             algorithms=['RS256'],
#             audience="f8448f27-dd2a-4a38-937b-3ceca9cfd89f",
#             issuer=f"https://sts.windows.net/YOUR_TENANT_ID/"
#         )
#         print("Token is valid:", decoded_token)
#     except Exception as e:
#         print("Invalid token:", e)

# # Example usage
# token = "EwBoA8l6BAAUbDba3x2OMJElkF7gJ4z/VbCPEz0AAekCzSNRh+0BoLwipzfMARYQWImBEzO6L5kPqBH4zscBhzVDwsCJVO/hlAciGRioGAvtfSQP0idGO5HcwXg6muU4SEDBtdNot/zr2o6E+EPdYByXWc1FlI8daqGuMYFx+kdMnyTyhjBL/cXhkfB0t88X/vOGiKrnK/5hAQa1ukijcwGhGvHqQ03F5cH+9ky9YI/4gjsdjjBJCGIjc/su3zCeMI0jNOIAA8PjpLlun96zrUyQLjtOp8TsQ7Ycjy498EIYE6LC06fPBrKEwtDhyMu+mzpIzIBR8WuZFyvpa+3rVjl+7P043jkKgWFcpJaNelIakQbezZC3zfgINhzAVZwQZgAAENdn8vIWjA7QNfNdlNx2nk8wAtwXo7a4b8xZzWUNcdC4bttMrh9WoZnOrzdNuYLxQBhRTayRvHxGNda2q8iEXl38AHaxHL/pSV/83ym2QJiQY8VsfLe3+jTLYTscIYAM0tR+MAamUTewlCYxYgxSC+bmvHzU6DkO7PzUkojkWhKFyRZdrEiAUMg935d/q0yi1Kx3RPg5q7TRTMFlOsV3AHF2gADLQYrH/k7/gHMc/hmfAW8eYfbC3pfdo+/Vey9KChyWIH1iqaJbibxPvJMa77Mq/+CNNCCCjXSWCmB71S+4TKeSXpaXuAEFklA7FqBOc5cAq0tzwXNZKpCGbrIz+ONI11KTeupPZOOMZjYyUxTp1uBQE2xWoB9XpkOn9JYsBLiytiSLWcCpuiMY2x4353VVEeMIFz/nt15STqQkKHD8tiFBtAD92MZA9b70yI6nEw8rFpxSyG1SRCKj/vf2UAUzUiZetWyO+aRkSm/8tR2L+zqiY318uJYChRwf1wgWRylB9CJq0Ek9NNOElv5/HObS4HsXmvaTb/D2x5P13ELA8HsCJgK7d5s7UaYcJeQ3WepDVE5sLsy0908ZfJxNXlST1kdTBVoxLn/5lXzXztKi7qbAxwrXQpnbCCf1iojG2LG/LcKmmyaV6ZgONU3iu3X3UD5xhXmuGGBTS6C72OcSZVq5xxvfiucpDNm40WJ2T6CLFOCvK/jdhVnL5F22PdJlGhF/c0CYgg5p4MBLHlvaL+zdpGTHUHelZf39bQTpPp2xdgI="
# validate_token(token)
