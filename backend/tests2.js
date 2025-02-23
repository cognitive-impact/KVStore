import axios from 'axios';

const BASE_URL = 'http://localhost:3000';

const tests = async () => {
    try {
        console.log('--- Running Tests ---');

        // 1. Put test keys
        console.log('Test: PUT /put (Inserting test data)');
        await axios.post(`${BASE_URL}/put`, { key: 'users::12345::Alice::profile', value: 'Test Profile 1' });
        await axios.post(`${BASE_URL}/put`, { key: 'users::67890::Bob::profile', value: 'Test Profile 2' });
        await axios.post(`${BASE_URL}/put`, { key: 'users::54321::Alice::settings', value: 'Test Settings 1' });
        await axios.post(`${BASE_URL}/put`, { key: 'orders::10001::pending', value: 'Order Pending' });
        await axios.post(`${BASE_URL}/put`, { key: 'orders::10002::shipped', value: 'Order Shipped' });

        // 2. Test Prefix Search
        console.log('Test: GET /search_prefix (Find users::)');
        const prefixResponse = await axios.get(`${BASE_URL}/search_prefix?prefix=users::`);
        console.log('Response:', prefixResponse.data);

        // 3. Test Contains Filter
        console.log('Test: GET /search_filter (Contains "Alice")');
        const containsResponse = await axios.get(`${BASE_URL}/search_filter?prefix=users::&contains=Alice`);
        console.log('Response:', containsResponse.data);

        // 4. Test EndsWith Filter
        console.log('Test: GET /search_filter (EndsWith "profile")');
        const endsWithResponse = await axios.get(`${BASE_URL}/search_filter?prefix=users::&endswith=profile`);
        console.log('Response:', endsWithResponse.data);

        // 5. Test Combined Contains + EndsWith
        console.log('Test: GET /search_filter (Contains "Alice", EndsWith "profile")');
        const combinedResponse = await axios.get(`${BASE_URL}/search_filter?prefix=users::&contains=Alice&endswith=profile`);
        console.log('Response:', combinedResponse.data);

        console.log('--- All tests executed ---');
    } catch (err) {
        console.error('Test failed:', err.message);
    }
};

// Run tests
tests();
