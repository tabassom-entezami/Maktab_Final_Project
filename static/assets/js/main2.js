
const url = window.location.href
const searchform = document.getElementById('search-form')
const searchInput = document.getElementById('search-input')

const resultBox = document.getElementById('results-box')
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

const sendSearchData = function(){
    $.ajax({
        type:'POST',
        url:'searchresults/',
        data:{
            "csrfmiddlewaretoken":csrf,
            "game":game,
        },
        success: function(res){
            console.log(res.data)
            const data = res.data
            if (Array.isArray(data)){
                resultBox.innerHTML = ""
                console.log('we have an array')
                data.forEach(game=>{
                    resultBox.innerHTML +=`
                    <a href="${{url}}${game.pk}" class="item">
                    <div class="row mt-2 mb-2>"
                    <div class="col-2"></div>
                    <img src="${game.food_image}"</img>
                    <div class="col-10"></div>
                    <h5>${game.food_name}</h5>
                    </div></div></a>`
                    
                })
            } else {
                if (searchInput.value.length > 0){
                    resultBox.innerHTML = <b>${data}</b>
                } else {
                    resultBox.classList.add('not-visible')
                }
            }
        },
        error:function(err){
            console.log(err)
        }
    })

}


$("#search-input").on('keyup',function(){
    console.log($(this).text());

    if (resultBox.classList.contains('not-visible')){
        resultBox.classList.remove('not-visible')
    }

    sendSearchData(e.target.value)
})