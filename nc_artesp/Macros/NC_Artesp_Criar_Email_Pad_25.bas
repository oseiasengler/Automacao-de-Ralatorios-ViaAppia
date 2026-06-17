Attribute VB_Name = "NC_Artesp_Criar_Email_Pad_25"

' Para anexos: Content-ID = nome do ficheiro (PDF (cod).jpg -> pdf%20(cod).jpg).
Private Function NC_Email_CidMapi(ByVal caminhoCompleto As String) As String
    Dim nom As String, r As String
    nom = Mid(caminhoCompleto, InStrRev(caminhoCompleto, "\") + 1)
    r = Replace(nom, " ", "%20")
    If Len(r) >= 3 And LCase(Left(r, 3)) = "pdf" Then
        NC_Email_CidMapi = "pdf" & Mid(r, 4)
    ElseIf Len(r) >= 2 And LCase(Left(r, 2)) = "nc" Then
        NC_Email_CidMapi = "nc" & Mid(r, 3)
    Else
        NC_Email_CidMapi = LCase(r)
    End If
End Function

Sub NC_Artesp_Criar_Email_Padrao_Rotina_Artesp_2025()

    Dim myText As String
    Dim Assunto As String
    Dim pula As String: pula = Chr$(10)
    Dim i As Long, l As Long, x As Long
    Dim sFile As String, Spath As String
    Dim ultimalinha As Long

    Dim m As MailItem
    Dim reply As MailItem

    Dim Cod_fiscalizacao(1000) As String
    Dim Data_fiscalizacao(1000) As String