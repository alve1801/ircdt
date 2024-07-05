# Browser-based chat server

I was taking a shower yesterday when I realised that by using html forms and
some server-side formatting, it should be possible to create a (bad) (insecure)
chat application that does not execute any code on the client.

Lo and behold, after about an hour, this came out. The username of the client is
stored in a hidden form input, and gets ping-ponged (not a technical term)
between the server and client with each request.

Known issues:
- refreshing the page without using the button (eg with ctrl-R) resends the last
  message
- text encoding is not handled
