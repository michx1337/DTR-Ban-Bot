const { model, Schema, connect, set } = require('mongoose')
const ban = model('bans', new Schema({ id: String }, { versionKey: false }))
const kick = model('kick', new Schema({ id: String }, { versionKey: false }))
const express = require('express')
const { setTimeout } = require('timers')
const { time } = require('console')
const app = express()
const base = '/api'

set('strictQuery', true)
connect('ENTER YOUR MONGODB CONNECTION STRING HERE')

app.get('/', async function(req, res) {
  res.send({
    version: '1.0.0',
    endpoints: [{
      path: '/',
      details: 'Returns information on this API.'
    }, {
      path: '/api/bans/{userId}',
      details: 'Used for adding, deleting, and getting bans.'
    }, {
      path: '/api/ping',
      details: 'Returns the current ping and database size.'
    }, {
      path: '/api/add/{userId}',
      details: 'Adds a user to the database.'
    }, {
      path: '/api/delete/{userId}',
      details: 'Deletes a user from the database.'
    }, {
      path: '/api/check/{userId}',
      details: 'Checks if a user is in the database.'
    }, {
      path: '/api/list',
      details: 'Returns a list of all banned users.'
    }, {
      path: '/api/kick/{userId}',
      details: 'Kicks a user from the game.'
    }, {
      path: '/api/kick/check/{userId}',
      details: 'Checks if a user is kicked.'
    }]
  })
})

app.get(`${base}/ping`, async function(req, res) {
  const before = Date.now()
  const docs = await ban.find()
  const after = Date.now()

  res.send({
    ping: (after - before),
    documents: docs.length
  })
})

// add a banned id
app.get(`${base}/game/ban/add/:id`, async function(req, res) {
  const id = req.params.id
  const doc = new ban({ id })

  await doc.save()
    .catch(() => res.send({ added: false }))
    .then(() => res.send({ added: true }))
})

// delete a banned id
app.get(`${base}/game/ban/delete/:id`, async function(req, res) {
  const id = req.params.id
  await ban.findOneAndDelete({ id })
    .catch(() => res.send({ deleted: false }))
    .then(() => res.send({ deleted: true }))
})

// check banned id
app.get(`${base}/game/ban/check/:id`, async function(req, res) {
  const id = req.params.id
  const doc = await ban.findOne({ id })
  const code = !!doc ? 1 : 0

  res.send({ code })
})

// get banned ids
app.get(`${base}/game/ban/list`, async function(req, res) {
  const docs = await ban.find()
  const ids = docs.map(doc => doc.id)

  res.send({ ids })
})

// kick someone in game
app.get(`${base}/game/kick/add/:id`, async function(req, res) {
  const id = req.params.id
  const doc = new kick({ id })

  await doc.save()
  setTimeout(async function() {
    await kick.findOneAndDelete({ id })
      .catch(() => res.send({ kicked: false }))
      .then(() => res.send({ kicked: true }))
  }, 100);
})

// check if someone is kicked
app.get(`${base}/game/kick/check/:id`, async function(req, res) {
  const id = req.params.id
  const doc = await kick.findOne({ id })
  const code = !!doc ? 1 : 0

  res.send({ code })
})

app.listen(8080, function() {
  console.log('Server opened on port 8080.')
})
