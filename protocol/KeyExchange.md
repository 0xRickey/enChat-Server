# Key Exchange Protocol

## Client Message Structure

The client sends a **three-part message** to initiate a session. This separates encryption from signature verification to work within RSA size limits.

### Outer Message Format (sent over network)
```json
{
    "encrypted_message": "<base64-encoded-rsa-encrypted-data>",
    "signature": "<hex-encoded-signature>",
    "public_key": "<hex-encoded-der-public-key>"
}
```

**Field Descriptions:**
- `encrypted_message`: The core session data encrypted with server's RSA public key (base64-encoded)
- `signature`: RSA signature of the original message content (hex-encoded)
- `public_key`: Client's public key in DER format (hex-encoded) for signature verification

### Inner Message Format (what gets RSA-encrypted)
```json
{
    "M": {                              // M = MESSAGE
        "C": "START_SESSION",           // C = COMMAND
        "P": {                          // P = PAYLOAD
            "SK": "<session-key-uuid>", // SK = SESSION_KEY (UUID format)
            "SI": "<base64-session-id>", // SI = SESSION_ID (base64-encoded random bytes)
            "CN": 0,                    // CN = CLIENT_NONCE (integer)
            "TS": 1753250489            // TS = TIMESTAMP (unix timestamp)
        },
        "T": {                          // T = METADATA
            "RI": "<request-id-uuid>"   // RI = REQUEST_ID (UUID for logging/tracking)
        }
    }
}
```

### Field Abbreviations Reference
| Abbreviation | Full Name | Description |
|-------------|-----------|-------------|
| M | MESSAGE | Top-level message container |
| C | COMMAND | The action being requested |
| P | PAYLOAD | Core session establishment data |
| T | METADATA | Additional message metadata |
| SK | SESSION_KEY | Symmetric key for subsequent AES communications |
| SI | SESSION_ID | Unique identifier for this session |
| CN | CLIENT_NONCE | Client's nonce counter (starts at 0) |
| TS | TIMESTAMP | Unix timestamp when message was created |
| RI | REQUEST_ID | Unique identifier for request tracking |

### Why This Format?
- **Size Optimization**: Abbreviated field names reduce message size to fit RSA encryption limits (~214 bytes)
- **Security Separation**: Signature is verified separately from decryption
- **Compact JSON**: No spaces, minimal field names for maximum efficiency

## Server Response
Note that this will be encrypted using the provided symmetric key (AES encryption)
```json
{
    "CIPHERTEXT": {
        "MESSAGE": {
            "RESPONSE": "START_SESSION_SUCCESS",
            "PAYLOAD": {
                "SESSION_ID": "random bytes",
                "NONCE": 0,          // Server side Nonce
                "TIMESTAMP": 1234568 // Time of message being sent
            }
        },
        "SIGNATURE": "server_priv_key(hash(message))"
    },
    "IV": "WIEOFJ0NG2U94H"
}
```

## Protocol Flow
1. **Client** creates session data with abbreviated field names
2. **Client** RSA-encrypts the compact message with server's public key
3. **Client** signs the original message content with its private key
4. **Client** packages encrypted message + signature + public key and sends to server
5. **Server** verifies signature using provided public key
6. **Server** RSA-decrypts the message content
7. **Server** responds with AES-encrypted confirmation
8. **All subsequent communications** use AES encryption with the established session key
