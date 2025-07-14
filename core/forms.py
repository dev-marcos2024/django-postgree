from django import  forms
from django.core.mail import  EmailMessage
from core.models import Produto

class ContatoForm(forms.Form):
    nome = forms.CharField(
        label='Nome',
        max_length=100,
        widget = forms.TextInput(attrs={
            'class': 'form-control-lg'
        })
    )
    email = forms.EmailField(
        label='E-mail',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control-lg'
        })
    )
    assunto = forms.CharField(
        label='Assunto',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control-lg'
        })
    )
    mensagem = forms.CharField(label='Mensagem',widget=forms.Textarea(attrs={'rows':'3'}))

    def send_email(self):
        data = self.cleaned_data

        corpo = (
            f"Nome: {data['nome']}\n"
            f"E-mail: {data['email']}\n"
            f"Assunto: {data['assunto']}\n"
            f"Mensagem:\n{data['mensagem']}"
        )

        mail = EmailMessage(
            subject='Email enviado com sucesso!',
            body=corpo,
            from_email='contato@seudominio.com.br',
            to=['contato@seudominio.com.br'],
            headers={'Reply-To': data['email']},
        )
        mail.send()

class ProdutoMoselForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'estoque', 'imagem']