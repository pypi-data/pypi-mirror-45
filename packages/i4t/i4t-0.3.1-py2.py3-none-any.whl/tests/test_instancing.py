## @file test_instancing.py
# @brief Tests for I4T Instancing
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


from   i4t.core.instancing import InstancingToken, InstancingTokenClaims, InstancingWarrant
from   pbose.core.PbWS import PbWS
import pytest
from   tests.fixtures.pbwk import keys_sign
import time
from   datetime import datetime


################################################################################
# PbWS
################################################################################


@pytest.mark.parametrize('key', keys_sign, indirect=True)
def test_instancing_token(key):
  # Instancing Token Claim
  it_claims = InstancingTokenClaims(
    iss='iss',
    sub='sub',
    aud='aud',
    # exp=datetime.utcnow(),
    # nbf=datetime.utcnow(),
    # iat=datetime.utcnow(),
    jti='jti',
    public=b'public',
    private=b'private',
    public_key=key.public_key.protobuf,
    serial='serial',
    sku='sku',
    upc=1,
    manufacturer_name='manufacturer_name',
    manufacturer_location='manufacturer_location',
    manufacturer_lot='manufacturer_lot',
    manufacturer_line='manufacturer_line',
  )
  # Instancing Token
  it = InstancingToken(
    protected=b'protected',
    header=b'header',
    payload=it_claims.to_bytes(),
    signature=b'signature',
  )
  # Instancing Warrant
  iw = InstancingWarrant(
    version=1,
    token=it.protobuf,
    private_key=key.protobuf,
  )
  # sign
  temp = PbWS(payload=b'0123456789')
  temp.sign(iw.private_key)
  # verify
  temp.verify(iw.private_key.public_key)
  # InstancingToken
  it = iw.token
  temp.verify(it.payload.public_key)


@pytest.mark.parametrize('key', keys_sign, indirect=True)
def test_instancing_warrant(key):
  iw = InstancingWarrant.from_key_with_claims(
    key=key,
    iss='iss',
    sub='sub',
    aud='aud',
    # exp=datetime.utcnow(),
    # nbf=datetime.utcnow(),
    # iat=datetime.utcnow(),
    jti='jti',
    public=b'public',
    private=b'private',
    serial='serial',
    sku='sku',
    upc=1,
    manufacturer_name='manufacturer_name',
    manufacturer_location='manufacturer_location',
    manufacturer_lot='manufacturer_lot',
    manufacturer_line='manufacturer_line',
  )
  iw.sign(key)

# @pytest.mark.parametrize('key', keys_sign, indirect=True)
# def test_instancing_warrant_alg(key):
#   iw = InstancingWarrant.generate_for_alg_with_claims(
#     alg=alg,
#     iss='iss',
#     sub='sub',
#     aud='aud',
#     exp=time_now,
#     nbf=time_now,
#     iat=time_now,
#     jti='jti',
#     public=b'public',
#     private=b'private',
#     serial='serial',
#     sku='sku',
#     upc=1,
#     manufacturer_name='manufacturer_name',
#     manufacturer_location='manufacturer_location',
#     manufacturer_lot='manufacturer_lot',
#     manufacturer_line='manufacturer_line',
#   )
#   iw.sign(key)

# @pytest.mark.parametrize('key', keys_sign, indirect=True)
# def test_instancing_warrant_should_fail(key):
#   iw = InstancingWarrant.from_key_with_claims(
#     key=key,
#     public_key=key.public_key, # public key is a bad claim in this instance
#   )
#   assert False
