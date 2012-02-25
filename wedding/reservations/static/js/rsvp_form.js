// JavaScript to support the RSVP form for my wedding.
//   author: Luke Sneeringer
//   copyright: 2012, Luke Sneeringer
(function() {
    // if any "regret" options are selected, then
    // hide the entreé line...
    var food_visibility = function(animate) {
        if (typeof animate === 'undefined') {
            animate = true
        }
        
        // iterate over each invitee and see whether or not he is coming
        $('section.invitee').each(function() {
            var $invitee_form = $(this)
            var $food_option = $invitee_form.find('.field').eq(1)
            
            // is the "regret" button checked"?
            if ($invitee_form.find('.field').eq(0).find('input[value="False"]:checked').length > 0) {
                // this person can't come; don't show their food options
                if (animate) {
                    $food_option.slideUp()
                }
                else {
                    $food_option.hide()
                }
            }
            else {
                // there will never be a no-animate case for re-display
                $food_option.slideDown()
            }
        })
    }

    // once the page is loaded, set everything up...
    $(document).ready(function() {
        food_visibility(false)
        // whenever a form option changes, check to see if the food option
        // needs to be shown or hidden
        $('input[type="radio"]').click(function() {
            food_visibility()
        })
        
        // hide the vegetarian and gluten free options at the start;
        // these are limited-availability...
        $('section.invitee').each(function() {
            var $invitee_form = $(this)
            var $food = $invitee_form.find('.form-input').eq(1)
            var $special_options = $food.find('li').slice(3)
            
            // sanity check: has the person *selected* a special meal?
            // if so, don't hide them...
            if ($special_options.find('input:checked').length > 0) {
                return
            }
            
            // hide the extra options to begin
            $special_options.hide()
            
            // add a "special" link for those with vegetarian / gluten free needs
            var $special = $('<span class="special">(specialty meals also available)</span>').insertBefore($special_options.eq(0))
            $special.click(function() {
                $special_options.show('normal')
                $special.remove()
            })
        })
    })
})()