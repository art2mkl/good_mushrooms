//$('.alert').hide()
const loc_origin = window.location.origin
$('.answer').hide()
$('.poisoned').hide()
$('.edible').hide()
$('.diag').hide()


//-------------------------------------------------------------------------------------------------------------
//-----------------------------------------    FUNCTIONS     --------------------------------------------------
//-------------------------------------------------------------------------------------------------------------



function get_models() {
    //--------------------------------------------------------------------------------------------------------------
    //Select Models in current project
    //--------------------------------------------------------------------------------------------------------------         
        fetch(`${loc_origin}/prediction/choosemodel/`).then( response => {
            response.json().then( data => {
                
                let optionHTML = '';
                
                for (let model of data.models) {
                    optionHTML += '<option value="'+ model.id + '">' + `${model.name} accuracy : ${model.accuracy.toFixed(2)}, precision : ${model.precision.toFixed(2)}` + '</option>';
                }
                choose_model.innerHTML = optionHTML;

            });
        });
    }
//get_models()




//Actions sur le formulaire lors de la validation
$('form').on('submit', e => {

    //Annuler le rafraichissement automatique de la page
    e.preventDefault();

    //si valeurs pas complète
    $('.answer').hide()
    $('.poisoned').hide()
    $('.edible').hide()
    $('.diag').hide()

    if ($('select').eq(0).val() == "no-value"
        || $('select').eq(1).val() == "no-value"
        || $('select').eq(2).val() == "no-value"
        || $('select').eq(3).val() == "no-value"
        || $('select').eq(4).val() == "no-value")
         
        {
        console.log('c est vide')
        $('.answer').fadeIn()
        $('.diag').fadeIn()
        $('.cross').on('click', () => {
            $('.answer').fadeOut()
        })
    } else {
        sendmodel = $('select').eq(0).val()
        _odor = $('select').eq(1).val()
        _habitat = $('select').eq(2).val()
        _cap_color = $('select').eq(3).val()
        _bruises = $('select').eq(4).val()
        

        url = `${loc_origin}/prediction/predict/${sendmodel}/${_odor}/${_habitat}/${_cap_color}/${_bruises}`

        fetch(url).then((Response) => {
            return Response.json()
        }).then((data) => {
            prediction = (data.prediction[0].predict);
            console.log(prediction)
            if (prediction == 'edible') {
                $('.answer').fadeIn()
                $('.edible').fadeIn()    
            } else if (prediction == 'poisoned') {
                $('.answer').fadeIn()     
                $('.poisoned').fadeIn()
            }
            $('.cross').on('click', () => {
                $('.answer').fadeOut()
            })
        })

    }
})