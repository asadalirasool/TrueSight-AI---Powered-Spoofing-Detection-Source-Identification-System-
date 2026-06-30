"""
Test suite for microservices architecture verification
"""

import asyncio
import pytest
import aiohttp
from typing import Dict, Any

class MicroservicesTester:
    """Test microservices architecture components"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"  # Gateway URL
        self.session: aiohttp.ClientSession = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def test_gateway_health(self) -> bool:
        """Test API gateway health"""
        try:
            async with self.session.get(f"{self.base_url}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✓ Gateway health check passed: {data}")
                    return True
                else:
                    print(f"✗ Gateway health check failed: {response.status}")
                    return False
        except Exception as e:
            print(f"✗ Gateway health check error: {str(e)}")
            return False
    
    async def test_service_discovery(self) -> bool:
        """Test service discovery"""
        try:
            async with self.session.get(f"{self.base_url}/services") as response:
                if response.status == 200:
                    data = await response.json()
                    services = data.get("services", [])
                    print(f"✓ Service discovery found {len(services)} services:")
                    for service in services:
                        print(f"  - {service['name']} ({service['status']})")
                    return len(services) > 0
                else:
                    print(f"✗ Service discovery failed: {response.status}")
                    return False
        except Exception as e:
            print(f"✗ Service discovery error: {str(e)}")
            return False
    
    async def test_auth_service(self) -> bool:
        """Test authentication service"""
        try:
            # Test health endpoint
            async with self.session.get("http://localhost:8004/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✓ Auth service health: {data['status']}")
                    
                    # Test registration
                    register_data = {
                        "username": "testuser",
                        "email": "test@example.com",
                        "password": "testpass123"
                    }
                    async with self.session.post(
                        "http://localhost:8004/register",
                        json=register_data
                    ) as reg_response:
                        if reg_response.status in [200, 400]:  # 400 if user exists
                            print("✓ Auth service registration endpoint working")
                            return True
                        else:
                            print(f"✗ Auth service registration failed: {reg_response.status}")
                            return False
                else:
                    print(f"✗ Auth service health check failed: {response.status}")
                    return False
        except Exception as e:
            print(f"✗ Auth service test error: {str(e)}")
            return False
    
    async def test_detection_service(self) -> bool:
        """Test detection service"""
        try:
            async with self.session.get("http://localhost:8001/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✓ Detection service health: {data['status']}")
                    print(f"  Models loaded: {data['models_loaded']}")
                    return True
                else:
                    print(f"✗ Detection service health check failed: {response.status}")
                    return False
        except Exception as e:
            print(f"✗ Detection service test error: {str(e)}")
            return False
    
    async def test_forensic_service(self) -> bool:
        """Test forensic service"""
        try:
            async with self.session.get("http://localhost:8002/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✓ Forensic service health: {data['status']}")
                    print(f"  Modules loaded: {data['modules_loaded']}")
                    return True
                else:
                    print(f"✗ Forensic service health check failed: {response.status}")
                    return False
        except Exception as e:
            print(f"✗ Forensic service test error: {str(e)}")
            return False
    
    async def test_blockchain_service(self) -> bool:
        """Test blockchain service"""
        try:
            async with self.session.get("http://localhost:8003/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✓ Blockchain service health: {data['status']}")
                    print(f"  Modules loaded: {data['modules_loaded']}")
                    return True
                else:
                    print(f"✗ Blockchain service health check failed: {response.status}")
                    return False
        except Exception as e:
            print(f"✗ Blockchain service test error: {str(e)}")
            return False
    
    async def run_all_tests(self) -> Dict[str, bool]:
        """Run all microservices tests"""
        results = {}
        
        print("Starting microservices architecture tests...\n")
        
        # Test individual services
        results["auth_service"] = await self.test_auth_service()
        results["detection_service"] = await self.test_detection_service()
        results["forensic_service"] = await self.test_forensic_service()
        results["blockchain_service"] = await self.test_blockchain_service()
        
        # Test gateway and discovery
        results["gateway_health"] = await self.test_gateway_health()
        results["service_discovery"] = await self.test_service_discovery()
        
        # Summary
        passed = sum(results.values())
        total = len(results)
        print(f"\n{'='*50}")
        print(f"TEST SUMMARY: {passed}/{total} tests passed")
        print(f"Success rate: {(passed/total)*100:.1f}%")
        print(f"{'='*50}")
        
        return results

async def main():
    """Main test function"""
    async with MicroservicesTester() as tester:
        results = await tester.run_all_tests()
        return all(results.values())

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)