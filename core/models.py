import os
import shutil
from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from versatileimagefield.fields import VersatileImageField, PPOIField
from versatileimagefield.image_warmer import VersatileImageFieldWarmer


class Base(models.Model):
    criacao = models.DateField(auto_now_add=True)
    modificacao = models.DateField(auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True


class Produto(Base):
    nome = models.CharField('Nome', max_length=100)
    preco = models.DecimalField('Preço', max_digits=8, decimal_places=2)
    estoque = models.IntegerField('Estoque')

    imagem = VersatileImageField(
        'Imagem',
        upload_to='produtos/',
        blank=True,
        null=True
    )
    imagem_ppoi = PPOIField()  # ponto de foco da imagem

    slug = models.SlugField('Slug', max_length=100, blank=True, editable=False)

    def __str__(self):
        return self.nome


@receiver(pre_save, sender=Produto)
def set_slug_and_cleanup_old_image(sender, instance, **kwargs):
    instance.slug = slugify(instance.nome)

    if not instance.pk:
        return

    try:
        old_instance = Produto.objects.get(pk=instance.pk)
    except Produto.DoesNotExist:
        return

    if old_instance.imagem and old_instance.imagem != instance.imagem:
        imagem_path = old_instance.imagem.path
        imagem_dir = os.path.dirname(imagem_path)
        if os.path.exists(imagem_dir):
            shutil.rmtree(imagem_dir)


@receiver(post_save, sender=Produto)
def generate_image_variations(sender, instance, **kwargs):
    if instance.imagem:
        warmer = VersatileImageFieldWarmer(
            instance_or_queryset=instance,
            rendition_key_set='produto_image',
            image_attr='imagem'
        )
        warmer.warm()


@receiver(post_delete, sender=Produto)
def delete_image_folder(sender, instance, **kwargs):
    if instance.imagem:
        imagem_path = instance.imagem.path
        imagem_dir = os.path.dirname(imagem_path)
        if os.path.exists(imagem_dir):
            shutil.rmtree(imagem_dir)
