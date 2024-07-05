# Browser-based chat server

I was taking a shower yesterday when I realised that by using html forms and
some server-side formatting, it should be possible to create a (bad) (insecure)
chat application that does not execute any code on the client.

Lo and behold, after about an hour, this came out. The username of the client is
stored in a hidden form input, and gets ping-ponged (not a technical term)
between the server and client with each request.

Name came around because I was thinking of how to mess around with irc, I took
it to mean "I really can't do this" - turns out, I can :3

Known issues:
- refreshing the page without using the button (eg with ctrl-R) resends the last
  message
- text encoding is not handled
