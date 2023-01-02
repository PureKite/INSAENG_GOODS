function addFile(obj){
    $('.file-list').empty();
    let htmlData = '';
    var maxFileCnt = 4;   // 첨부파일 최대 개수
    var curFileCnt = obj.files.length;  // 현재 선택된 첨부파일 개수

    // 첨부파일 개수 확인
    if (curFileCnt > maxFileCnt) {
        swal("첨부파일은 최대 " + maxFileCnt + "개 까지 첨부 가능합니다.");
        document.querySelector("input[type=file]").value = '';
    } else {
        for (const file of obj.files) {
            // 첨부파일 검증
            if (validation(file)) {
                let htmlData = '';
                htmlData += '<p class="name">' + file.name + '</p>';
                $('.file-list').append(htmlData);
            } else {
                document.querySelector("input[type=file]").value='';
                continue;
            }
        }
    }
}
/* 첨부파일 검증 */
function validation(obj){
    const fileTypes = ['image/gif', 'image/jpeg', 'image/png', 'image/bmp', 'image/tif'];
    if (obj.name.length > 100) {
        swal("파일명이 100자 이상인 파일은 제외되었습니다.");
        return false;
    } else if (obj.size > (100 * 1024 * 1024)) {
        swal("최대 파일 용량인 100MB를 초과한 파일은 제외되었습니다.");
        document.querySelector("input[type=file]").value='';
        return false;
    } else if (obj.name.lastIndexOf('.') == -1) {
        swal("확장자가 없는 파일은 제외되었습니다.");
        return false;
    } else if (!fileTypes.includes(obj.type)) {
        swal("첨부가 불가능한 파일은 제외되었습니다.");
        return false;
    } else {
        return true;
    }
}

function p_del(num){
    swal({
        title:'게시글을 정말로 삭제하시겠습니까?',
        text: "",
        icon:"info",
        buttons: ["아니오", "네"]
    }).then(function(result){
    //var res = confirm('게시글을 정말로 삭제하시겠습니까?');
        if(result){
            swal({title:"삭제 완료", text:"성공적으로 삭제되었습니다."
            }).then((value) => {
                if(value){
                    window.location.href = "/article/delete/"+num;
                }
            })
        }
    })
}
function p_udt(num){
    window.location.href = "/article/update/"+num
}
$(function(){
    $(".thumbs a").click(function(){          
        var imgPath = $(this).children("img");
        console.log(imgPath)
        $("#mainImg>img").attr("src", imgPath.attr("src"));//.attr("alt", imgPath.attr("alt"));
        return false;                       
    });
});

const Update = (id) => {
    let Update = document.querySelector(`.Update${id}`);
    let Delete = document.querySelector(`.Delete${id}`);
    let CommentSubmit = document.querySelector(`.CommentSubmit${id}`);
    let UpdateCancel = document.querySelector(`.UpdateCancel${id}`);
    let Content = document.querySelector(`.Content${id}`);

    Update.style.display = 'none';
    Delete.style.display = 'none';
    CommentSubmit.style.display = 'inline-block';
    UpdateCancel.style.display = 'inline-block';
    Content.disabled = false;
    Content.style.border = '1px solid #ced4da';
}
const UpdateCancel = (id) => {
    let Update = document.querySelector(`.Update${id}`);
    let Delete = document.querySelector(`.Delete${id}`);
    let CommentSubmit = document.querySelector(`.CommentSubmit${id}`);
    let UpdateCancel = document.querySelector(`.UpdateCancel${id}`);
    let Content = document.querySelector(`.Content${id}`);

    CommentSubmit.style.display = 'none';
    UpdateCancel.style.display = 'none';
    Update.style.display = 'inline-block';
    Delete.style.display = 'inline-block';
    Content.disabled = true;
    Content.style.border = 'none';
}
const CommentSubmit = (id) => {
    let Content = document.querySelector(`.Content${id}`).value;
    let param = {
        'id': id,
        'Comment_content': Content,
    }
    var time = new Date();
    $.ajax({
        url : "/article/updatecomment/",
        type : 'POST',
        headers: {
            'X-CSRFTOKEN' : '{{ csrf_token }}'
        },
        data : JSON.stringify(param),
        success:function(data){
            if (data.result == 'ok'){
                let Update = document.querySelector(`.Update${id}`);
                let Delete = document.querySelector(`.Delete${id}`);
                let CommentSubmit = document.querySelector(`.CommentSubmit${id}`);
                let UpdateCancel = document.querySelector(`.UpdateCancel${id}`);
                let Content = document.querySelector(`.Content${id}`);
                let d = document.querySelector(`.Date${id}`);
                
                CommentSubmit.style.display = 'none';
                UpdateCancel.style.display = 'none';
                Update.style.display = 'inline-block';
                Delete.style.display = 'inline-block';
                Content.style.border = 'none';
                const date = new Date();
                const year = date.getFullYear();
                const month = date.getMonth() + 1;
                const day = date.getDate(); 
                const hours = date.getHours();
                const minutes = date.getMinutes();
                if (minutes < 10){
                    minutes = '0' + str(minutes);
                }
                d.value = year+'년 '+month+'월 '+day+'일 '+(hours%12)+':'+minutes+' '+date.toLocaleTimeString('ko-kr').slice(0,2);
                Content.disabled = true;
            }
        },
        error: function(){
            alert('실패');
        }
    });
}
$(function() {
    $('.text_area').each(function() {
        $(this).height($(this).prop('scrollHeight'));
    });
    $('.text_area').on('keydown keyup', function() {
        $(this).height($(this).prop('scrollHeight'));
    });
    // $('#id_Comment_content').on('keydown keyup', function() {
    //     $(this).height($(this).prop('scrollHeight'));
    // });
});