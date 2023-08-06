## @file PbWS.py
# @brief Protobuf Web Signature
#
# @copyright
# Copyright 2018 PbOSE <https://pbose.io>
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


from   pbose.core import pb_object
from   pbose.core.PbWA import PbWSHeaderAlg
from   pbose.core.PbWK import PbWK
from   pbose.exceptions import AlreadySignedException
from   pbose.protobuf import PbWS_pb2


################################################################################
# PbWS
################################################################################


class PbWS(pb_object):


  __protobuf__ = PbWS_pb2.PbWS


  # @special_property('header', PbWSHeader, PbWS_pb2.PbWSHeader)


  @property
  def header(self):
    return PbWSHeader.from_bytes(self.protobuf.header)


  @header.setter
  def header(self, header):
    if isinstance(header, PbWS_pb2.PbWSHeader):
      header = PbWSHeader(header)
    if isinstance(header, PbWSHeader):
      self.protobuf.header = header.to_bytes()
    else:
      raise TypeError("Not a valid PbWS header.")


  @property
  def protected(self):
    return PbWSHeader.from_bytes(self.protobuf.protected)


  @protected.setter
  def protected(self, protected):
    if isinstance(protected, PbWS_pb2.PbWSHeader):
      protected = PbWSHeader(protected)
    if isinstance(protected, PbWSHeader):
      self.protobuf.protected = protected.to_bytes()
    else:
      raise TypeError("Not a valid PbWS protected header.")


  @property
  def signed(self):
    return self.signature != b''


  def sign(self, key):
    self.protected = PbWSHeader(
      jwk=key.public_key,
    )
    self._sign(key)

  def _sign(self, key):
    if self.signed:
      raise AlreadySignedException()
    data = self.protobuf.protected + self.protobuf.payload
    signature = key.sign(data=data)
    self.signature = signature


  def verify(self, key):
    data = self.protobuf.protected + self.protobuf.payload
    signature = self.protobuf.signature
    key.verify(data=data, signature=signature)


################################################################################
# PbWSHeader
################################################################################


class PbWSHeader(pb_object):


  __protobuf__ = PbWS_pb2.PbWSHeader


  @classmethod
  def init_protobuf_with_properties_before(cls, **properties):
    if properties['jwk'] and isinstance(properties['jwk'], PbWK):
      properties['jwk'] = properties['jwk'].protobuf
    return properties


  @property
  def jwk(self):
    return PbWK(self.protobuf.jwk)


  @jwk.setter
  def jwk(self, jwk):
    if isinstance(jwk, PbWS_pb2.PbWK):
      jwk = PbWK(jwk)
    if isinstance(jwk, PbWK):
      self.protobuf.jwk.CopyFrom(jwk.protobuf)
    else:
      raise TypeError("Not a valid PbWK.")
