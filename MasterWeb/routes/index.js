var express = require('express');
var router = express.Router();

const {spawn} = require('child_process');

table = new Map();
tableStart = new Map();
tableEnd = new Map();

router.get('/', function(req, res, next) {
	// Convert table into array
	results = []
	keysIterator = table.keys()
	curr = keysIterator.next()
	while (!curr.done) {
		results.push({
		response: `${curr.value} = ${table.get(curr.value) === undefined ? ('Still cracking, been cracking for ' + (((new Date()) - tableStart.get(curr.value)) / 1000) + ' seconds') : (table.get(curr.value) + ' in ' + ((tableEnd.get(curr.value) - tableStart.get(curr.value)) / 1000) + ' seconds')}`,
		})
		curr = keysIterator.next()
	}
	
	// Send user to results screen
	res.render('index', {
		resultsList: results
	})
});

router.post('/', function(req, res, next) {
	const question = req.body['toCrack']
	
	// Handle new question
	if (!table.has(question)) {
		table.set(question, undefined)
		tableStart.set(question, new Date())
		
		// Begin distributed cracking
		const python = spawn('python3', ['../MasterCommunicator/MasterSubmit.py', question]);
		
		// Listen to stdout
		python.stdout.on('data', function (data) {
			table.set(question, data.toString())
			tableEnd.set(question, new Date())
		});
		
		python.stdout.on('close', function (data) {
			
		});
	}
	
	res.redirect('/');
});

module.exports = router;
