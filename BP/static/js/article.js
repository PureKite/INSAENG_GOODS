
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