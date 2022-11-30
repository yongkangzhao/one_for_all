const relations = [
    'strongly associates with occupation',
    'has strong persona',
    "strongly relates with personality type",
    "has strong ncskills",
    "strongly motivates to",
    "strongly motivates for",
    "strongly relates to skill",
    "as a result, person makes others feel",
    "relates to concepts",
    "is for job",
    "has strong traits",
    "is for field of study",
    "relates to fieldOfStudy",
    "relates to task"
]
// 
document.getElementById('submit').addEventListener('click', function() {
    const input = document.getElementById('question').value
    const output = document.getElementById('answer')
    
    for (let i = 0; i < relations.length; i++) {
        output.innerHTML += relations[i] + '<br><ui>'
        result = fetch('http://localhost:8000/generate/'+input+'/'+relations[i]).then(response => response.json()).then(data => {
            console.log(data)
            output.innerHTML += '<li>' + data[0] + '</li>'
        }
        )
        output.innerHTML += '</ui>'
        
    }
     
})