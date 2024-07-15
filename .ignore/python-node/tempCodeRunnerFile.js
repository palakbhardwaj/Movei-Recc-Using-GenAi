//Node js calls pyscript and passes name
//Pyscript prints Hello + name
//output is retured to nodejs

const {spawn}  = require('child_process')
const py = spawn('python3',['py-script.py', 'Pranjal'])

py.stdout.on('data',(data)=>{
    console.log(data.toString());
})

py.on('close',(code)=>{
    console.log(`Child process exited with code ${code}`)
})

