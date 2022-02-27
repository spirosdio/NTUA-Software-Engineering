#!/usr/bin/node

const program = require('commander');
const axios = require('axios').default;
const spawn = require('child_process').spawn;
var FormData = require('form-data');
var fs = require('fs');


program.version('1.0.0');

program
    .command('passesperstation')
    .option('--station <station>', 'from station')
    .option('--datefrom <startdate>', 'from start date')
    .option('--dateto <finishdate>', 'to finish date')
    .action(function(options) {

        if (options.station == undefined || options.datefrom == undefined || options.dateto == undefined) {
            if (options.station == undefined){
                console.log("Must define station using '--station' option")
            }
            if (options.datefrom == undefined){
                console.log("Must define datefrom using '--datefrom' option")
            }
            if (options.dateto == undefined){
                console.log("Must define dateto using '--dateto' option")
            }
            return
        }

        let config = {
            method: 'get',
            url: 'http://localhost:9103/interoperability/api/PassesPerStation/' +
                ((options.station != undefined) ? options.station : '') +
                ((options.datefrom != undefined) ? '/' + options.datefrom : '') +
                ((options.dateto != undefined) ? '/' + options.dateto : '') 
        }
        axios(config)
            .then(res => {
                console.log(res.data)
            })
            .catch(err => {
                console.log("Status code: " + err.response.status)
                if (err.response.status == 400 || err.response.status == 401 || err.response.status == 402)
                    console.log(err.response.data)
                if (err.response.status == 404)
                    console.log("Page Not Found")
            })
    })

program
    .command('passescost')
    .option('--op1 <op1>', 'op1')
    .option('--op2 <op2>', 'op2')
    .option('--datefrom <startdate>', 'from start date')
    .option('--dateto <finishdate>', 'to finish date')
    .action(function(options) {

        if (options.op1 == undefined || options.op2 == undefined || options.datefrom == undefined || options.dateto == undefined) {
            if (options.op1 == undefined){
                console.log("Must define first operator using '--op1' option")
            }
            if (options.op2 == undefined){
                console.log("Must define second operator using '--op2' option")
            }
            if (options.datefrom == undefined){
                console.log("Must define datefrom using '--datefrom' option")
            }
            if (options.dateto == undefined){
                console.log("Must define dateto using '--dateto' option")
            }
            return
        }

        let config = {
            method: 'get',
            url: 'http://localhost:9103/interoperability/api/PassesCost/' +
                ((options.op1 != undefined) ? options.op1 : '') +
                ((options.op2 != undefined) ? '/' + options.op2 : '') +
                ((options.datefrom != undefined) ? '/' + options.datefrom : '') +
                ((options.dateto != undefined) ? '/' + options.dateto : '') 
        }
        axios(config)
            .then(res => {
                console.log(res.data)
            })
            .catch(err => {
                console.log("Status code: " + err.response.status)
                if (err.response.status == 400 || err.response.status == 401 || err.response.status == 402)
                    console.log(err.response.data)
                if (err.response.status == 404)
                    console.log("Page Not Found")
            })
    })

program
    .command('passesanalysis')
    .option('--op1 <op1>', 'op1')
    .option('--op2 <op2>', 'op2')
    .option('--datefrom <startdate>', 'from start date')
    .option('--dateto <finishdate>', 'to finish date')
    .action(function(options) {

        if (options.op1 == undefined || options.op2 == undefined || options.datefrom == undefined || options.dateto == undefined) {
            if (options.op1 == undefined){
                console.log("Must define first operator using '--op1' option")
            }
            if (options.op2 == undefined){
                console.log("Must define second operator using '--op2' option")
            }
            if (options.datefrom == undefined){
                console.log("Must define datefrom using '--datefrom' option")
            }
            if (options.dateto == undefined){
                console.log("Must define dateto using '--dateto' option")
            }
            return
        }

        let config = {
            method: 'get',
            url: 'http://localhost:9103/interoperability/api/PassesAnalysis/' +
                ((options.op1 != undefined) ? options.op1 : '') +
                ((options.op2 != undefined) ? '/' + options.op2 : '') +
                ((options.datefrom != undefined) ? '/' + options.datefrom : '') +
                ((options.dateto != undefined) ? '/' + options.dateto : '') 
        }
        axios(config)
            .then(res => {
                console.log(res.data)
            })
            .catch(err => {
                console.log("Status code: " + err.response.status)
                if (err.response.status == 400 || err.response.status == 401 || err.response.status == 402)
                    console.log(err.response.data)
                if (err.response.status == 404)
                    console.log("Page Not Found")
            })
    })

program
    .command('chargesby')
    .option('--op1 <op1>', 'op1')
    .option('--datefrom <startdate>', 'from start date')
    .option('--dateto <finishdate>', 'to finish date')
    .action(function(options) {

        if (options.op1 == undefined || options.datefrom == undefined || options.dateto == undefined) {
            if (options.op1 == undefined){
                console.log("Must define operator using '--op1' option")
            }
            if (options.datefrom == undefined){
                console.log("Must define datefrom using '--datefrom' option")
            }
            if (options.dateto == undefined){
                console.log("Must define dateto using '--dateto' option")
            }
            return
        }

        let config = {
            method: 'get',
            url: 'http://localhost:9103/interoperability/api/ChargesBy/' +
                ((options.op1 != undefined) ? options.op1 : '') +
                ((options.datefrom != undefined) ? '/' + options.datefrom : '') +
                ((options.dateto != undefined) ? '/' + options.dateto : '') 
        }
        axios(config)
            .then(res => {
                console.log(res.data)
            })
            .catch(err => {
                console.log("Status code: " + err.response.status)
                if (err.response.status == 400 || err.response.status == 401 || err.response.status == 402)
                    console.log(err.response.data)
                if (err.response.status == 404)
                    console.log("Page Not Found")
            })
    })

program
    .command('resetstations')
    .description('resets stations')
    .action(function() {

        let config = {
            method: 'post',
            url: 'http://localhost:9103/interoperability/api/admin/resetstations'
        }
        axios(config)
            .then(res => {
                console.log(res.data)
            })
            .catch(err => {
                console.log("Status code: " + err.response.status)
                if (err.response.status == 400 || err.response.status == 401 || err.response.status == 402)
                    console.log(err.response.data)
                if (err.response.status == 404)
                    console.log("Page Not Found")
            })
    })

program
    .command('resetvehicles')
    .action(function() {

        let config = {
            method: 'post',
            url: 'http://localhost:9103/interoperability/api/admin/resetvehicles'
        }
        axios(config)
            .then(res => {
                console.log(res.data)
            })
            .catch(err => {
                console.log("Status code: " + err.response.status)
                if (err.response.status == 400 || err.response.status == 401 || err.response.status == 402)
                    console.log(err.response.data)
                if (err.response.status == 404)
                    console.log("Page Not Found")
            })
    })

program
    .command('resetpasses')
    .action(function() {

        let config = {
            method: 'post',
            url: 'http://localhost:9103/interoperability/api/admin/resetpasses'
        }
        axios(config)
            .then(res => {
                console.log(res.data)
            })
            .catch(err => {
                console.log("Status code: " + err.response.status)
                if (err.response.status == 400 || err.response.status == 401 || err.response.status == 402)
                    console.log(err.response.data)
                if (err.response.status == 404)
                    console.log("Page Not Found")
            })
    })

program
    .command('healthcheck')
    .action(function() {

        let config = {
            method: 'get',
            url: 'http://localhost:9103/interoperability/api/admin/healthcheck'
        }
        axios(config)
            .then(res => {
                console.log(res.data)
            })
            .catch(err => {
                console.log("Status code: " + err.response.status)
                if (err.response.status == 400 || err.response.status == 401 || err.response.status == 402)
                    console.log(err.response.data)
                if (err.response.status == 404)
                    console.log("Page Not Found")
            })
    })

program
    .command('admin')
    .option('--passesupd', 'option for admin that lets you upload a csv file with passes')
    .option('--source <path/to/file..>', 'path to file')
    .action(function(options) {

        const process = spawn('python', ['./python_hack.py', 'upload', options.source.toString()]);

        process.stdout.on('data', data => {
            console.log(data.toString());
        });
        
    })


program.parse(process.argv);