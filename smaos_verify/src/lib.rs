use wasm_bindgen::prelude::*;
use ed25519_dalek::{VerifyingKey, Signature, Verifier};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
pub struct VerificationResult {
    pub valid: bool,
    pub message: String,
}

#[wasm_bindgen]
pub fn verify_receipt(receipt_json: &str, public_key_pem: &str) -> String {
    // 1. Parse receipt, remove signature field for hashing
    let mut payload: serde_json::Value = serde_json::from_str(receipt_json).unwrap();
    let sig_hex = payload["signature"].as_str().unwrap_or("");
    payload["signature"] = serde_json::Value::String("".to_string());
    
    // 2. Verify Ed25519 Signature
    let verifying_key = VerifyingKey::from_pkcs8_pem(public_key_pem).unwrap();
    let signature = Signature::from_bytes(&hex::decode(sig_hex).unwrap().try_into().unwrap());
    
    match verifying_key.verify(serde_json::to_string(&payload).unwrap().as_bytes(), &signature) {
        Ok(_) => serde_json::to_string(&VerificationResult { 
            valid: true, 
            message: "✅ Cryptographic wire-truth verified. Receipt is authentic.".to_string() 
        }).unwrap(),
        Err(_) => serde_json::to_string(&VerificationResult { 
            valid: false, 
            message: "❌ Signature mismatch. Receipt may be tampered with.".to_string() 
        }).unwrap(),
    }
}
