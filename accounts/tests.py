from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Property, VendorProfile
import json

User = get_user_model()


class PropertyFilterTestCase(TestCase):
    """Test cases for property filtering and search"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create vendor user
        self.vendor_user = User.objects.create_user(
            username='testvendor',
            email='vendor@test.com',
            password='testpass123',
            role='vendor'
        )
        self.vendor_profile = VendorProfile.objects.create(
            user=self.vendor_user,
            company_name='Test Properties Ltd'
        )
        
        # Create test properties
        self.property1 = Property.objects.create(
            vendor=self.vendor_profile,
            title='Modern Apartment in Lagos',
            description='Beautiful 3-bedroom apartment',
            property_type='apartment',
            price=50000000,
            address='123 Victoria Island',
            city='Lagos',
            state='Lagos',
            bedrooms=3,
            bathrooms=2,
            area=120,
            is_available=True
        )
        
        self.property2 = Property.objects.create(
            vendor=self.vendor_profile,
            title='Luxury Duplex in Abuja',
            description='Spacious 5-bedroom duplex',
            property_type='duplex',
            price=120000000,
            address='456 Asokoro',
            city='Abuja',
            state='FCT',
            bedrooms=5,
            bathrooms=4,
            area=300,
            is_available=True
        )
        
        self.property3 = Property.objects.create(
            vendor=self.vendor_profile,
            title='Land for Sale in Ibadan',
            description='Prime land for development',
            property_type='land',
            price=20000000,
            address='789 Ring Road',
            city='Ibadan',
            state='Oyo',
            bedrooms=0,
            bathrooms=0,
            area=1000,
            is_available=True
        )
        
        self.property4 = Property.objects.create(
            vendor=self.vendor_profile,
            title='Apartment in Lagos (Unavailable)',
            description='Sold apartment',
            property_type='apartment',
            price=45000000,
            address='321 Lekki',
            city='Lagos',
            state='Lagos',
            bedrooms=2,
            bathrooms=2,
            area=100,
            is_available=False
        )
    
    def test_property_search_view_exists(self):
        """Test that property search view is accessible"""
        response = self.client.get(reverse('property_search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'property_search.html')
    
    def test_filter_by_location_city(self):
        """Test filtering properties by city"""
        response = self.client.get(reverse('property_search'), {'location': 'Lagos'})
        self.assertEqual(response.status_code, 200)
        properties = response.context['properties']
        # Should return only available Lagos properties (property1, not property4 as it's unavailable)
        self.assertEqual(len(properties), 1)
        self.assertIn(self.property1, properties)
    
    def test_filter_by_location_state(self):
        """Test filtering properties by state"""
        response = self.client.get(reverse('property_search'), {'location': 'Oyo'})
        self.assertEqual(response.status_code, 200)
        properties = response.context['properties']
        self.assertEqual(len(properties), 1)
        self.assertIn(self.property3, properties)
    
    def test_filter_by_property_type(self):
        """Test filtering by property type"""
        response = self.client.get(reverse('property_search'), {'property_type': 'duplex'})
        self.assertEqual(response.status_code, 200)
        properties = response.context['properties']
        self.assertEqual(len(properties), 1)
        self.assertIn(self.property2, properties)
    
    def test_filter_by_min_price(self):
        """Test filtering by minimum price"""
        response = self.client.get(reverse('property_search'), {'min_price': '60000000'})
        self.assertEqual(response.status_code, 200)
        properties = response.context['properties']
        self.assertEqual(len(properties), 1)
        self.assertIn(self.property2, properties)
    
    def test_filter_by_max_price(self):
        """Test filtering by maximum price"""
        response = self.client.get(reverse('property_search'), {'max_price': '30000000'})
        self.assertEqual(response.status_code, 200)
        properties = response.context['properties']
        self.assertEqual(len(properties), 1)
        self.assertIn(self.property3, properties)
    
    def test_filter_by_price_range(self):
        """Test filtering by price range"""
        response = self.client.get(reverse('property_search'), {
            'min_price': '40000000',
            'max_price': '60000000'
        })
        self.assertEqual(response.status_code, 200)
        properties = response.context['properties']
        self.assertEqual(len(properties), 1)
        self.assertIn(self.property1, properties)
    
    def test_combined_filters(self):
        """Test multiple filters together"""
        response = self.client.get(reverse('property_search'), {
            'location': 'Lagos',
            'property_type': 'apartment',
            'max_price': '60000000'
        })
        self.assertEqual(response.status_code, 200)
        properties = response.context['properties']
        self.assertEqual(len(properties), 1)
        self.assertIn(self.property1, properties)
    
    def test_search_query(self):
        """Test search functionality"""
        response = self.client.get(reverse('property_search'), {'q': 'Modern'})
        self.assertEqual(response.status_code, 200)
        properties = response.context['properties']
        self.assertEqual(len(properties), 1)
        self.assertIn(self.property1, properties)
    
    def test_only_available_properties_shown(self):
        """Test that only available properties are displayed"""
        response = self.client.get(reverse('property_search'))
        self.assertEqual(response.status_code, 200)
        properties = list(response.context['properties'])
        self.assertEqual(len(properties), 3)  # Only 3 available properties
        self.assertNotIn(self.property4, properties)
    
    def test_pagination(self):
        """Test pagination functionality"""
        # Create more properties to test pagination
        for i in range(15):
            Property.objects.create(
                vendor=self.vendor_profile,
                title=f'Property {i}',
                description=f'Description {i}',
                property_type='apartment',
                price=10000000 + (i * 1000000),
                address=f'Address {i}',
                city='Lagos',
                state='Lagos',
                bedrooms=2,
                bathrooms=1,
                area=80,
                is_available=True
            )
        
        response = self.client.get(reverse('property_search'))
        self.assertEqual(response.status_code, 200)
        properties = response.context['properties']
        self.assertEqual(len(properties), 12)  # 12 per page
        self.assertTrue(properties.has_next())
    
    def test_invalid_price_filter(self):
        """Test that invalid price values are handled gracefully"""
        response = self.client.get(reverse('property_search'), {
            'min_price': 'invalid',
            'max_price': 'also_invalid'
        })
        self.assertEqual(response.status_code, 200)
        # Should return all available properties
        properties = list(response.context['properties'])
        self.assertEqual(len(properties), 3)


class PropertyAPITestCase(TestCase):
    """Test cases for property API endpoint"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create vendor user
        self.vendor_user = User.objects.create_user(
            username='apivendor',
            email='apivendor@test.com',
            password='testpass123',
            role='vendor'
        )
        self.vendor_profile = VendorProfile.objects.create(
            user=self.vendor_user,
            company_name='API Test Properties'
        )
        
        # Create test property
        self.property = Property.objects.create(
            vendor=self.vendor_profile,
            title='API Test Property',
            description='Test description',
            property_type='apartment',
            price=30000000,
            address='API Street',
            city='Lagos',
            state='Lagos',
            bedrooms=3,
            bathrooms=2,
            area=150,
            is_available=True
        )
    
    def test_api_endpoint_returns_json(self):
        """Test that API endpoint returns JSON response"""
        response = self.client.get(reverse('property_api'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
    
    def test_api_response_structure(self):
        """Test that API response has correct structure"""
        response = self.client.get(reverse('property_api'))
        data = json.loads(response.content)
        
        self.assertIn('count', data)
        self.assertIn('num_pages', data)
        self.assertIn('current_page', data)
        self.assertIn('has_next', data)
        self.assertIn('has_previous', data)
        self.assertIn('results', data)
        
        self.assertEqual(data['count'], 1)
        self.assertEqual(len(data['results']), 1)
    
    def test_api_property_data(self):
        """Test that API returns correct property data"""
        response = self.client.get(reverse('property_api'))
        data = json.loads(response.content)
        
        property_data = data['results'][0]
        self.assertEqual(property_data['title'], 'API Test Property')
        self.assertEqual(property_data['property_type'], 'apartment')
        self.assertEqual(property_data['city'], 'Lagos')
        self.assertEqual(property_data['bedrooms'], 3)
    
    def test_api_filter_by_location(self):
        """Test API filtering by location"""
        response = self.client.get(reverse('property_api'), {'location': 'Lagos'})
        data = json.loads(response.content)
        
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['city'], 'Lagos')
    
    def test_api_filter_by_price(self):
        """Test API filtering by price range"""
        response = self.client.get(reverse('property_api'), {
            'min_price': '20000000',
            'max_price': '40000000'
        })
        data = json.loads(response.content)
        
        self.assertEqual(data['count'], 1)


class VendorPropertyListTestCase(TestCase):
    """Test cases for vendor property management"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create vendor user
        self.vendor_user = User.objects.create_user(
            username='listvendor',
            email='listvendor@test.com',
            password='testpass123',
            role='vendor'
        )
        self.vendor_profile = VendorProfile.objects.create(
            user=self.vendor_user,
            company_name='List Test Properties'
        )
        
        # Create properties
        Property.objects.create(
            vendor=self.vendor_profile,
            title='Available Property',
            property_type='apartment',
            price=30000000,
            address='123 Street',
            city='Lagos',
            state='Lagos',
            bedrooms=2,
            bathrooms=1,
            area=100,
            is_available=True
        )
        
        Property.objects.create(
            vendor=self.vendor_profile,
            title='Unavailable Property',
            property_type='duplex',
            price=50000000,
            address='456 Avenue',
            city='Abuja',
            state='FCT',
            bedrooms=4,
            bathrooms=3,
            area=200,
            is_available=False
        )
    
    def test_vendor_must_be_logged_in(self):
        """Test that vendor must be authenticated"""
        response = self.client.get(reverse('vendor_property_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_vendor_can_view_properties(self):
        """Test that vendor can view their properties"""
        self.client.login(username='listvendor', password='testpass123')
        response = self.client.get(reverse('vendor_property_list'))
        self.assertEqual(response.status_code, 200)
        properties = list(response.context['properties'])
        self.assertEqual(len(properties), 2)
    
    def test_vendor_filter_by_status(self):
        """Test filtering by availability status"""
        self.client.login(username='listvendor', password='testpass123')
        response = self.client.get(reverse('vendor_property_list'), {'status': 'available'})
        self.assertEqual(response.status_code, 200)
        properties = list(response.context['properties'])
        self.assertEqual(len(properties), 1)