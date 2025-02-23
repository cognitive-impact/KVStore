import express from 'express';
import bodyParser from 'body-parser';
import level from 'level';

const app = express();
const db = level('../leveldb', { valueEncoding: 'json' });
app.use(express.json({limit: '50mb'}));
app.use(express.urlencoded({limit: '50mb', extended: true}));

app.use(bodyParser.json({ limit: '50mb' }));
app.use(bodyParser.urlencoded({ limit: '50mb', extended: true }));

app.get("/", async(req, res) => {
    res.json({"status": "ok"})
})
// Get a value by key
app.get('/get/:key', async (req, res) => {
    try {
        const value = await db.get(req.params.key);
        res.json({ key: req.params.key, value });
    } catch (err) {
        if (err.notFound) {
            res.status(404).json({ error: 'Key not found' });
        } else {
            res.status(500).json({ error: err.message });
        }
    }
});

// Put a key-value pair
app.post('/put', async (req, res) => {
    const { key, value } = req.body;
    if (!key || value === undefined) {
        return res.status(400).json({ error: 'Key and value are required' });
    }
    try {
        await db.put(key, value);
        res.json({ success: true, key, value });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Delete a key
app.delete('/delete/:key', async (req, res) => {
    try {
        await db.del(req.params.key);
        res.json({ success: true, key: req.params.key });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Batch operations
app.post('/batch', async (req, res) => {
    const operations = req.body;
    if (!Array.isArray(operations)) {
        return res.status(400).json({ error: 'Batch payload must be an array' });
    }
    try {
        await db.batch(operations);
        res.json({ success: true });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Get multiple values by keys
app.post('/getall', async (req, res) => {
    console.log(req.body)
    const keys  = req.body;
    if (!Array.isArray(keys)) {
        return res.status(400).json({ error: 'Keys must be an array' });
    }
    try {
        const values = await Promise.all(
            keys.map(async key => {
                try {
                    const value = await db.get(key);
                    return { key, value };
                } catch (err) {
                    if (err.notFound) {
                        return { key, error: 'Key not found' };
                    }
                    throw err;
                }
            })
        );
        res.json(values);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Stream all key-value pairs
app.get('/stream', (req, res) => {
    res.setHeader('Content-Type', 'application/json');
    res.write('[');
    let first = true;
    
    db.createReadStream()
        .on('data', ({ key, value }) => {
            if (!first) res.write(',');
            first = false;
            res.write(JSON.stringify({ key, value }));
        })
        .on('end', () => {
            res.write(']');
            res.end();
        })
        .on('error', err => {
            res.status(500).json({ error: err.message });
        });
});

app.get('/search_prefix', (req, res) => {
    const { prefix } = req.query; // Example: 'known_'
    if (!prefix) {
        return res.status(400).json({ error: 'Prefix is required' });
    }

    const results = [];
    
    db.createReadStream({ gte: prefix, lt: prefix + '\xFF' }) // Efficient prefix search
        .on('data', ({ key, value }) => {
            results.push({ key, value });
        })
        .on('end', () => {
            res.json(results);
        })
        .on('error', err => {
            res.status(500).json({ error: err.message });
        });
});


app.get('/search_filter', (req, res) => {
    console.log("Called search filter.")
    const { prefix, suffix, contains } = req.query;


    if (!prefix) {
        return res.status(400).json({ error: 'Prefix is required' });
    }

    let use_suffix = suffix 

    if (!suffix) {
        use_suffix = prefix+ '\xFF'
    } else {
        use_suffix = use_suffix + '\xFF'
    }
    console.log(prefix, use_suffix, contains)
    const results = [];

    db.createReadStream({ gte: prefix, lt: use_suffix }) // Efficient prefix search
        .on('data', ({ key, value }) => {
            if (!contains || key.includes(contains)) {  // Only filter if 'contains' is provided
                results.push({ key, value });
            }
        })
        .on('end', () => {
            res.json(results);
        })
        .on('error', err => {
            res.status(500).json({ error: err.message });
        });
});

app.get('/exists/:key', async (req, res) => {
    const { key } = req.params;
    let exists = false;

    db.createKeyStream({ gte: key, lte: key })
        .on('data', () => {
            exists = true; // Found the key
        })
        .on('end', () => {
            res.json({ key, exists });
        })
        .on('error', (err) => {
            res.status(500).json({ error: err.message });
        });
});

//More.

const PORT = 3000;
app.listen(PORT, () => console.log(`LevelDB API running on port ${PORT}`));
// main()

