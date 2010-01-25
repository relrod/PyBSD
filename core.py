#!/usr/bin/env python
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, defer
import sys, os, re, pprint

class PyBSD(irc.IRCClient):
   nickname = 'PyBSD'

   def connectionMade(self):
      irc.IRCClient.connectionMade(self)

   def connectionLost(self, reason):
      irc.IRCClient.connectionLost(self, reason)

   def signedOn(self):
      for channel in self.factory.channels:
         self.join(channel)

   def privmsg(self, who, channel, msg):
      # Do some simple user parsing.
      if "!" in who and "@" in who:
         user_split_a = who.split("!", 1)
         user_split_b = user_split_a[1].split("@", 1)
         nick = user_split_a[0]
         user = user_split_b[0]
         host = user_split_b[1]
         print nick + ": " + msg

      if msg.startswith("!"):
         msg = re.sub('^!', '', msg)
         command, _, args = msg.partition(' ')
         func = getattr(self, "cmdhook_" + command, None)
         if func is None:
            return
         d = defer.maybeDeferred(func, args)

         if channel == self.nickname:
            args = [nick]
         else:
            args = [channel, nick]
         d.addCallbacks(self._send_message(*args), self._show_error(*args))

   def _send_message(self, target, nick=None):
      def callback(msg):
         if nick:
            msg = nick + ": " + msg
         self.msg(target, msg)
      return callback

   def _show_error(self, target, nick=None):
      def errback(f):
         msg = f.getErrorMessage()
         if nick:
            msg = nick + ": " + msg
         self.msg(target, msg)
      return errback
   
   def cmdhook_test(self, args):
      return "HI!"


class PyBSDFactory(protocol.ClientFactory):
   protocol = PyBSD

   def clientConnectionLost(self, connector, reason): connector.connect()

if __name__ == "__main__":
   bot = PyBSDFactory()
   bot.nickname = "PyBSD"
   bot.channels = ["#codeblock"]
   reactor.connectTCP("platinum.eighthbit.net", 6667, bot)
   reactor.run()
