document
    .getElementById("generateBtn")
    .addEventListener("click", generateQR);


// UTF-8 강제 처리
qrcode.stringToBytes = function(str) {

    const utf8 = [];

    for (let i = 0; i < str.length; i++) {

        let charcode = str.charCodeAt(i);

        if (charcode < 0x80) {

            utf8.push(charcode);

        } else if (charcode < 0x800) {

            utf8.push(
                0xc0 | (charcode >> 6),
                0x80 | (charcode & 0x3f)
            );

        } else if (
            charcode < 0xd800 ||
            charcode >= 0xe000
        ) {

            utf8.push(
                0xe0 | (charcode >> 12),
                0x80 | ((charcode >> 6) & 0x3f),
                0x80 | (charcode & 0x3f)
            );

        } else {

            i++;

            charcode =
                0x10000 +
                (
                    ((charcode & 0x3ff) << 10)
                    |
                    (str.charCodeAt(i) & 0x3ff)
                );

            utf8.push(
                0xf0 | (charcode >> 18),
                0x80 | ((charcode >> 12) & 0x3f),
                0x80 | ((charcode >> 6) & 0x3f),
                0x80 | (charcode & 0x3f)
            );
        }
    }

    return utf8;
};


function generateQR() {

    const text =
        document
        .getElementById("text")
        .value
        .trim();

    if (!text) {

        alert("텍스트를 입력하세요.");
        return;
    }

    const qrDiv =
        document.getElementById("qrcode");

    qrDiv.innerHTML = "";

    try {

        // version auto / ECC Medium
        const qr = qrcode(0, 'M');

        qr.addData(text);
		
        qr.make();

        qrDiv.innerHTML =
            qr.createImgTag(8, 16)

    } catch (e) {

        console.error(e);

        alert(
            "QR 생성 실패: 데이터가 너무 길거나 인코딩 문제가 있습니다."
        );
    }
}