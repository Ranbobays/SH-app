const form = document.getElementById("uploadForm");
const resultBox = document.getElementById("result");
const legalNotes = document.getElementById("legalNotes");

form.addEventListener("submit", function (e) {
  e.preventDefault();

  // UI loading state
  resultBox.innerHTML = "<p>Memproses dokumen...</p>";
  legalNotes.innerHTML = "<li>Menganalisis pasal...</li>";

  // simulasi proses AI / backend
  setTimeout(() => {
    resultBox.innerHTML = `
      <h3>Ringkasan Kontrak</h3>
      <p>Kontrak mengandung klausul pembayaran, kewajiban kerja, dan terminasi sepihak.</p>
    `;

    legalNotes.innerHTML = `
      <li>Pembayaran: wajib dilakukan dalam 30 hari</li>
      <li>Terminasi: dapat diputus sepihak dengan notice 7 hari</li>
      <li>Risiko: terdapat klausul penalti keterlambatan</li>
    `;
  }, 1500);
});