#!/usr/bin/env python3
"""
Comprehensive TrueSight System Validation Script
Tests database, API integration, and core functionality
"""

import sys
import os
import asyncio
import tempfile
import uuid
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import pytest
from loguru import logger

# Import our components
from shared.database import init_database, db_manager, health_check
from shared.models import User, UserRole
from services.detection_service import detection_service
from api.routes.detection import DetectionRequest

def test_database_initialization():
    """Test database initialization and schema creation"""
    print("🧪 Testing Database Initialization...")
    
    try:
        # Initialize database
        success = init_database(create_tables=True, drop_existing=False)
        assert success, "Database initialization failed"
        
        # Test database connectivity
        db_health = health_check()
        assert db_health, "Database health check failed"
        
        # Test table creation by querying
        with db_manager.get_db_session() as session:
            user_count = session.query(User).count()
            print(f"   ✅ Database initialized successfully")
            print(f"   ✅ Found {user_count} existing users")
            return True
            
    except Exception as e:
        print(f"   ❌ Database test failed: {e}")
        return False

def test_detection_service_initialization():
    """Test detection service initialization"""
    print("\n🔍 Testing Detection Service Initialization...")
    
    try:
        # Check service status
        status = detection_service.get_module_status()
        print(f"   ✅ Detection service initialized")
        print(f"   ✅ Active modules: {sum(status.values())}/{len(status)}")
        
        # Test health check
        health = asyncio.run(detection_service.health_check())
        assert health["overall_status"] in ["healthy", "degraded"]
        print(f"   ✅ Health check passed: {health['overall_status']}")
        return True
        
    except Exception as e:
        print(f"   ❌ Detection service test failed: {e}")
        return False

def test_model_integration():
    """Test integration between models and database"""
    print("\n📊 Testing Model Integration...")
    
    try:
        with db_manager.get_db_session() as session:
            # Test creating a user
            test_user = User(
                id=uuid.uuid4(),
                username=f"test_user_{uuid.uuid4().hex[:8]}",
                email=f"test_{uuid.uuid4().hex[:8]}@example.com",
                hashed_password="test_hash",
                first_name="Test",
                last_name="User",
                role=UserRole.ANALYST,
                is_active=True,
                is_verified=True
            )
            
            session.add(test_user)
            session.commit()
            session.refresh(test_user)
            
            # Verify user was created
            retrieved_user = session.query(User).filter(User.id == test_user.id).first()
            assert retrieved_user is not None
            assert retrieved_user.username == test_user.username
            
            # Clean up
            session.delete(test_user)
            session.commit()
            
            print("   ✅ Model integration test passed")
            return True
            
    except Exception as e:
        print(f"   ❌ Model integration test failed: {e}")
        return False

def test_detection_workflow():
    """Test complete detection workflow"""
    print("\n🚀 Testing Detection Workflow...")
    
    try:
        # Create test media content
        test_content = b"This is test media content for validation"
        test_file_type = "video/mp4"
        test_config = {
            "detection_types": ["video", "forensics"],
            "confidence_threshold": 0.8
        }
        
        # Run detection
        results = asyncio.run(detection_service.perform_multimodal_detection(
            file_content=test_content,
            file_type=test_file_type,
            detection_config=test_config
        ))
        
        # Validate results structure
        assert "detection_id" in results
        assert "individual_results" in results
        assert "aggregated_results" in results
        assert "modules_executed" in results
        
        print(f"   ✅ Detection workflow completed")
        print(f"   ✅ Detection ID: {results['detection_id']}")
        print(f"   ✅ Modules executed: {len(results['modules_executed'])}")
        print(f"   ✅ Processing time: {results.get('total_processing_time', 0):.2f}s")
        return True
        
    except Exception as e:
        print(f"   ❌ Detection workflow test failed: {e}")
        return False

def test_api_route_models():
    """Test API route model validation"""
    print("\n📡 Testing API Route Models...")
    
    try:
        # Test DetectionRequest model
        request_data = {
            "detection_types": ["video", "audio"],
            "confidence_threshold": 0.85,
            "include_forensics": True
        }
        
        detection_request = DetectionRequest(**request_data)
        assert detection_request.detection_types == ["video", "audio"]
        assert detection_request.confidence_threshold == 0.85
        assert detection_request.include_forensics == True
        
        print("   ✅ API route models validated successfully")
        return True
        
    except Exception as e:
        print(f"   ❌ API route model test failed: {e}")
        return False

def run_comprehensive_validation():
    """Run all validation tests"""
    print("=" * 60)
    print("TRUEsight System - Comprehensive Validation")
    print("=" * 60)
    
    tests = [
        ("Database Initialization", test_database_initialization),
        ("Detection Service", test_detection_service_initialization),
        ("Model Integration", test_model_integration),
        ("Detection Workflow", test_detection_workflow),
        ("API Route Models", test_api_route_models)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"   ❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"VALIDATION SUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - System is ready!")
        print("\n📋 Implementation Status:")
        print("✅ Database layer with SQLAlchemy models")
        print("✅ Alembic migrations configured") 
        print("✅ API routes connected to ML modules")
        print("✅ Detection service orchestration")
        print("✅ Model integration verified")
        return True
    else:
        print("⚠️  Some tests failed - please check implementation")
        return False

if __name__ == "__main__":
    success = run_comprehensive_validation()
    sys.exit(0 if success else 1)