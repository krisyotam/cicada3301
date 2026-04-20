Error.prototype.what=function(){ return this.message; };

class InvalidArgumentError extends TypeError {
  constructor(message) {
    super(message);
    this.name = "std::invalid_argument";
  }
}


function stoi(s){
    console.log(" stoi",s)
    let i = parseInt(s,10);
    if(isNaN(i)) throw new InvalidArgumentError('stoi');
    return i;
}

window.cin_input_queue=[];

function cin_write(s){
    console.log(" cin_write",s)
    cout(s+"\r\n");
    window.cin_input_queue.push(""+s);
}


function cin_internal_now(){
    let val = window.cin_input_queue.shift();//pop front
    console.log(" cin_internal_now",val,typeof val)
    return val;//pop front
}

async function cin_internal(){
    const cin_deferred = () => new Promise(
            resolve => {
                let foo = ()=>{
                    if(window.cin_input_queue.length>0) return resolve(cin_internal_now());
                    else setTimeout(foo,250);
                };
                foo();
            }
    );
    return cin_deferred();
}

function cin_html_fixfocus(){
    setInterval( ()=>{
        let el = document.getElementById('cin-input');
        if(el!==null) el.focus();
    },50);
}

function cin_html_submitprompt(){
    let el = document.getElementById('cin-input');
    let input = el.value;
    el.remove();
    cin_write(input);
}
function cin_html_addprompt(){
    let el = document.getElementById('cin-input');
    if(el!==null) el.remove();
    el = document.createElement('input');
    el.id='cin-input';
    el.onkeypress=function(e){
        if(e.keyCode===13){
            cin_html_submitprompt();
        }
    };
    let parent = document.getElementById('terminal');
    parent.appendChild(el);
    el.focus();
}

async function cin(){
    cin_html_addprompt();
    return await cin_internal();
}


function cout(s){
    document.getElementById('terminal').innerText += s;
    console.log(s);
}

window.endl = "\r\n";

function terminate(ex){
    cout("Aborted"+endl)
    throw ex;
}

async function call_with_exceptions(func){
    try{
        await func();
    }catch(ex){
        cout("terminate called after throwing an instance of '"+ex.name+"'"+endl);
        cout("what():  "+ex.what()+endl)
        terminate(ex);
    }
}

