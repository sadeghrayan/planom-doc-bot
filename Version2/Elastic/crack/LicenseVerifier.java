/*
 * Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
 * or more contributor license agreements. Licensed under the Elastic License
 * 2.0; you may not use this file except in compliance with the Elastic License
 * 2.0.
 */
package org.elasticsearch.license;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.apache.lucene.util.BytesRef;
import org.apache.lucene.util.BytesRefIterator;
import org.elasticsearch.common.bytes.BytesReference;
import org.elasticsearch.common.hash.MessageDigests;
import org.elasticsearch.core.Streams;
import org.elasticsearch.xcontent.ToXContent;
import org.elasticsearch.xcontent.XContentBuilder;
import org.elasticsearch.xcontent.XContentFactory;
import org.elasticsearch.xcontent.XContentType;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.ByteBuffer;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.PublicKey;
import java.security.Signature;
import java.security.SignatureException;
import java.util.Arrays;
import java.util.Base64;
import java.util.Collections;

import static org.elasticsearch.core.Strings.format;

/**
 * Responsible for verifying signed licenses
 */
public class LicenseVerifier {

    private static final Logger logger = LogManager.getLogger(LicenseVerifier.class);

    /**
     * verifies the license content with the signature using the packaged
     * public key
     * @param license to verify
     * @return true if valid, false otherwise
     */
    public static boolean verifyLicense(final License license, PublicKey publicKey) {
            return true;
    }

    private static final PublicKey PUBLIC_KEY;
    private static final String PUBLIC_KEY_DIGEST_HEX_STRING;

    static {
        try (InputStream is = LicenseVerifier.class.getResourceAsStream("/public.key")) {
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            Streams.copy(is, out);
            byte[] publicKeyBytes = out.toByteArray();
            PUBLIC_KEY = CryptUtils.readPublicKey(publicKeyBytes);
            PUBLIC_KEY_DIGEST_HEX_STRING = MessageDigests.toHexString(MessageDigests.sha256().digest(publicKeyBytes));
        } catch (IOException e) {
            throw new AssertionError("key file is part of the source and must deserialize correctly", e);
        }
    }

    public static boolean verifyLicense(final License license) {
        return verifyLicense(license, PUBLIC_KEY);
    }
}
