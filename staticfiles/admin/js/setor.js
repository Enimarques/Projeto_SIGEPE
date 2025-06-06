django.jQuery(document).ready(function() {
    // Inicializa o Select2 nos campos de seleção
    django.jQuery('.select2').select2({
        theme: 'bootstrap-5',
        width: '100%'
    });

    // Atualiza a lista de responsáveis quando o tipo de setor muda
    django.jQuery('#id_tipo').on('change', function() {
        var tipo = django.jQuery(this).val();
        var responsavelSelect = django.jQuery('#id_nome_responsavel');
        
        // Limpa a seleção atual
        responsavelSelect.val(null).trigger('change');
        
        // Busca assessores do tipo selecionado via AJAX
        django.jQuery.ajax({
            url: '/recepcao/get_assessores/',
            data: {
                'tipo': tipo
            },
            dataType: 'json',
            success: function(data) {
                // Limpa as opções atuais
                responsavelSelect.empty();
                
                // Adiciona a opção vazia
                responsavelSelect.append(new Option('Selecione um responsável', '', true, true));
                
                // Adiciona as novas opções
                data.forEach(function(assessor) {
                    responsavelSelect.append(new Option(assessor.text, assessor.id, false, false));
                });
                
                // Atualiza o Select2
                responsavelSelect.trigger('change');
            }
        });
    });

    // Preenche os campos do responsável quando um assessor é selecionado
    django.jQuery('#id_nome_responsavel').on('change', function() {
        var assessorId = django.jQuery(this).val();
        
        if (assessorId) {
            django.jQuery.ajax({
                url: '/recepcao/get_assessor_info/',
                data: {
                    'assessor_id': assessorId
                },
                dataType: 'json',
                success: function(data) {
                    django.jQuery('#id_email').val(data.email);
                    django.jQuery('#id_funcao').val(data.funcao).trigger('change');
                    django.jQuery('#id_horario_entrada').val(data.horario_entrada);
                    django.jQuery('#id_horario_saida').val(data.horario_saida);
                }
            });
        }
    });
});
