import axios from 'axios';

const BASE_URL = 'http://localhost:3000';

const tests = async () => {
    try {
        console.log('--- Running Tests ---');

        // 1. Put a key-value pair
        console.log('Test: PUT /put');
        await axios.post(`${BASE_URL}/put`, { key: 'test_key', value: 'test_value' });

        // 2. Get the value by key
        console.log('Test: GET /get/test_key');
        const getResponse = await axios.get(`${BASE_URL}/get/test_key`);
        console.log('Response:', getResponse.data);

        // 3. Try getting a non-existent key
        console.log('Test: GET /get/missing_key (should 404)');
        try {
            await axios.get(`${BASE_URL}/get/missing_key`);
        } catch (error) {
            console.log('Expected error:', error.response.data);
        }

        // 4. Batch operation (put multiple keys)
        console.log('Test: POST /batch');
        await axios.post(`${BASE_URL}/batch`, [
            { type: 'put', key: 'batch_1', value: 'value_1' },
            { type: 'put', key: 'batch_2', value: 'value_2' }
        ]);

        // 5. Get multiple keys
        console.log('Test: POST /getall');
        const getAllResponse = await axios.post(`${BASE_URL}/getall`, ['batch_1', 'batch_2', 'non_existent']);
        console.log('Response:', getAllResponse.data);

        // 6. Prefix search
        console.log('Test: GET /search_prefix?prefix=batch_');
        const searchResponse = await axios.get(`${BASE_URL}/search_prefix?prefix=batch_`);
        console.log('Response:', searchResponse.data);

        // 7. Stream all key-value pairs
        console.log('Test: GET /stream');
        const streamResponse = await axios.get(`${BASE_URL}/stream`);
        console.log('Response:', streamResponse.data);

        // 8. Delete a key
        console.log('Test: DELETE /delete/test_key');
        await axios.delete(`${BASE_URL}/delete/test_key`);

        // 9. Confirm deletion
        console.log('Test: GET /get/test_key (should 404)');
        try {
            await axios.get(`${BASE_URL}/get/test_key`);
        } catch (error) {
            console.log('Expected error:', error.response.data);
        }

        console.log('--- All tests executed ---');
    } catch (err) {
        console.error('Test failed:', err.message);
    }
};

// Run tests
tests();
