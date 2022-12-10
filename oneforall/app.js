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
    
    // clear output
    output.innerHTML = ''


    let grid = document.createElement('div')
    grid.setAttribute('class', 'grid-container')
    output.appendChild(grid)

    for (let i = 0; i < relations.length; i++) {
        let card = document.createElement('div')
        card.setAttribute('class', 'grid-item')
        grid.appendChild(card)

        let relation = relations[i]
        let result = fetch('http://54.183.211.128:8000/generate/'+input+'/'+relations[i]).then(response => response.json()).then(data => {
            card.innerHTML += '<p><b>'+relation+'</b>: <ol>'

            for (let j = 0; j < data[relation].length; j++) {
                card.innerHTML += '<li>'+data[relation][j]+'</li>'
            }
            card.innerHTML += '</p>'
        }
        )
    }

     
})

