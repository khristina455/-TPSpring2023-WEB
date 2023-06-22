getHTML = (data) => {
    result = `<li class="q">
        <div class="row" id="answer-${data.id}">
        <div class="col-3 profile">
            <img src= "${data.avatar_url}" />
            <a href="#">${data.first_name} ${data.last_name}</a>
            <div class = "checkbox">
                Correct
                <input class="correct" data-qid="${data.qid}" data-aid="${data.id}" type="checkbox"`;
    if(!data.is_author) {
        result += `disabled`;
    }
    result += `>
            </div>
        </div>
        <div class="col-9 pt-2">
            <p class="text-q">
                ${data.content}
            </p>
        </div>
    </div>
    </li>`
    return result;
 }

const data = document.currentScript.dataset;
var centrifuge = new Centrifuge(data.address, {onRefresh: function(ctx, cb) {
        let promise = fetch("http://localhost:8002/centrifuge/refresh", {
            method: "POST"
        }).then(function(resp) {
            resp.json().then(function(data) {
                cb(data);
            });
        });
        }
 });

centrifuge.setToken(data.token);
centrifuge.subscribe(data.chan, function(message) {
    $("#answers").append(getHTML(message.data));
});
centrifuge.connect();