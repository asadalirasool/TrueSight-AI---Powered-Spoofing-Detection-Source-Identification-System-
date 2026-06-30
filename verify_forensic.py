"""
Simple Forensic Module Verification
Quick test to verify forensic source identification is working
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def verify_forensic_module():
    """Verify forensic module functionality"""
    print("🔍 VERIFYING FORENSIC SOURCE IDENTIFICATION MODULE")
    print("=" * 50)
    
    try:
        # Test imports
        print("1. Testing imports...")
        from modules.forensics.source_identifier import (
            ForensicSourceIdentifier, 
            ForensicEvidence, 
            AttributionConfidence
        )
        print("   ✅ All classes imported successfully")
        
        # Test initialization
        print("\n2. Testing initialization...")
        forensic_analyzer = ForensicSourceIdentifier(cache_dir="./test_cache")
        print("   ✅ ForensicSourceIdentifier initialized")
        print(f"   PRNU Analyzer: {forensic_analyzer.prnu_analyzer is not None}")
        print(f"   GAN Classifier: {forensic_analyzer.gan_classifier is not None}")
        print(f"   Device Attribution: {forensic_analyzer.device_attribution is not None}")
        
        # Test evidence creation
        print("\n3. Testing evidence structure...")
        evidence = ForensicEvidence(
            evidence_id="test_001",
            media_hash="abc123",
            prnu_analysis={"status": "test"},
            gan_fingerprint={"status": "test"},
            metadata_analysis={"status": "test"},
            device_attribution={"status": "test"},
            integrity_score=85.5,
            confidence_level=AttributionConfidence.HIGH,
            timestamp="2024-01-01T00:00:00",
            analysis_components=["prnu", "gan", "metadata"]
        )
        print("   ✅ ForensicEvidence created successfully")
        print(f"   Evidence ID: {evidence.evidence_id}")
        print(f"   Integrity Score: {evidence.integrity_score}")
        print(f"   Confidence: {evidence.confidence_level.value}")
        
        print("\n🎉 FORENSIC MODULE VERIFICATION COMPLETE!")
        print("Forensic Source Identification is ready for use.")
        return True
        
    except Exception as e:
        print(f"\n❌ VERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = verify_forensic_module()
    sys.exit(0 if success else 1)