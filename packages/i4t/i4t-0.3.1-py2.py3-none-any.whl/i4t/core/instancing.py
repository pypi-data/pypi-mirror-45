## @file instancing.py
# @brief I4T Instancing Token
#
# @copyright
# Copyright 2018 I4T <https://i4t.io>
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##


from   google.protobuf.timestamp_pb2 import Timestamp
from   i4t.protobuf import Instancing_pb2
from   pbose.core import pb_object
from   pbose.core.PbWK import PbWK
from   pbose.core.PbWS import PbWS


class InstancingToken(PbWS):


  TOKEN_TYPE = 'x.i4t.it'


  # def init_protobuf_with_properties_after(self, protobuf):
  #   assert protobuf.typ == INSTANCING_TOKEN_TYPE


  @property
  def payload(self):
    return InstancingTokenClaims.from_bytes(self.protobuf.payload)


  @payload.setter
  def payload(self, payload):
    if isinstance(payload, PbWS_pb2.InstancingTokenClaims):
      payload = InstancingTokenClaims(payload)
    if isinstance(payload, InstancingTokenClaims):
      self.protobuf.payload = payload.to_bytes()
    else:
      raise TypeError("Not a valid InstancingToken payload.")


class InstancingTokenClaims(pb_object):


  __protobuf__ = Instancing_pb2.InstancingTokenClaims


  @classmethod
  def init_protobuf_with_properties_before(cls, **properties):
    if 'iat' not in properties:
      iat = Timestamp()
      iat.GetCurrentTime()
      properties['iat'] = iat
    return properties


  @property
  def public_key(self):
    return PbWK(self.protobuf.public_key)


class InstancingWarrant(pb_object):


  __protobuf__ = Instancing_pb2.InstancingWarrant


  @classmethod
  def from_key_with_claims(cls, key, **properties):
    assert 'public_key' not in properties.keys()
    itc = InstancingTokenClaims(
      public_key=key.public_key.protobuf,
      **properties
    )
    it = InstancingToken(
      payload=itc.to_bytes(),
    )
    return cls(
      token=it.protobuf,
      private_key=key.protobuf,
    )


  @property
  def token(self):
    return InstancingToken(self.protobuf.token)


  @property
  def private_key(self):
    return PbWK(self.protobuf.private_key)


  @property
  def signed(self):
    return self.token.signed


  def sign(self, key):
    self.token.sign(key)


  def verify(self, key):
    self.token.verify(key)
