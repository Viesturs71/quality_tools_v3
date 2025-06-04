# quality_docs/services/pdf_signer.py


from pyhanko.sign import signers


def sign_pdf_document(input_pdf_path, certificate_path, password, signer_name=None):
    """
    Digitāli paraksta PDF failu, izmantojot .p12 sertifikātu.
    Atgriež parakstītā PDF faila ceļu.
    """
    output_pdf_path = input_pdf_path.replace('.pdf', '_signed.pdf')

    # Uzstāda parakstīšanas iestatījumus
    signer = signers.SimpleSigner.load_pkcs12(
        pfx_file=certificate_path,
        passphrase=password.encode('utf-8')
    )

    with open(input_pdf_path, 'rb') as inf, open(output_pdf_path, 'wb') as outf:
        pdf_signer = signers.PdfSigner(
            signers.PdfSignatureMetadata(field_name='Signature1'),
            signer=signer
        )
        pdf_signer.sign_pdf(inf, output=outf)

    return output_pdf_path
