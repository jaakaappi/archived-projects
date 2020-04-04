express = require('express')
require('dotenv').config()
var cors = require('cors')

const app = express()
app.use(cors());

app.get('/', (req, res) => res.send('Hello World!'))

app.listen(process.env.PORT, () => console.log(`Listening on port ${process.env.PORT}!`))