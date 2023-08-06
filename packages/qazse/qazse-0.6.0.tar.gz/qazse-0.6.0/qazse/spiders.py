#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------
#       项目名: qazse   
#       文件名: spiders 
#       作者  : Qazse 
#       时间  : 2019/4/13
#       主页  : http://qiiing.com 
#       功能  :
# ---------------------------------------------------
import qazse


def ask_get(resp_text,url, question_title_css='', question_content_css='', answers_css='', remove_keyword='', type='auto',
            coding=None):
    """
    问答提取工具
    :param resp_text:返回的内容
    :param question_title_css: 例如.question-name
    :param question_content_css:
    :param answers_css: list css样式
    :param remove_keyword: list
    :param type: 类型 baidu wukong zhihu auto
    :param coding:编码类型
    :return: list
    """
    from bs4 import BeautifulSoup

    wukong_question_title = '.question-name'
    wukong_question_content = '.question-text'
    wukong_answers = ['.answer-text']
    wukong_remove = ['分享', '举报', '展开全部', '\d+评论', '评论']

    baidu_question_title = '.ask-title'
    baidu_question_content = '.line.mt-5.q-content'
    baidu_answers = ['.line.content']
    baidu_remove = ['分享', '举报', '展开全部', '\d+评论', '评论']

    zhihu_question_title = '.QuestionHeader-title'
    zhihu_question_content = '.RichText.ztext'
    zhihu_answers = ['.RichContent-inner']
    zhihu_remove = ['分享', '举报', '展开全部', '\d+评论', '评论','谢邀','邀请']

    if type == 'auto':
        if 'baidu' in url:
            type = 'baidu'
        elif 'wukong' in url:
            type = 'wukong'
        elif 'zhidao.baidu.com' in url:
            type = 'zhihu'

    if type == 'baidu':
        question_title_css = baidu_question_title
        question_content_css = baidu_question_content
        answers_css = baidu_answers
        remove_keyword = baidu_remove
    elif type == 'wukong':
        question_title_css = wukong_question_title
        question_content_css = wukong_question_content
        answers_css = wukong_answers
        remove_keyword = wukong_remove
    elif type == 'zhihu':
        question_title_css = zhihu_question_title
        question_content_css = zhihu_question_content
        answers_css = zhihu_answers
        remove_keyword = zhihu_remove
    soup = BeautifulSoup(resp_text, features="lxml")
    question_title = soup.select_one(question_title_css).text
    question_title = qazse.text.remove_n_r(question_title)
    question_content = soup.select_one(question_content_css).text if (soup.select_one(question_content_css)) else ''
    question_content = qazse.text.remove_n_r(question_content)
    question_md5 = qazse.text.md5_str(question_title + question_content)
    answers = list()
    for css in answers_css:
        answers = answers + soup.select(css)
    answers_list = []
    for index, answer in enumerate(answers):
        answer = qazse.text.remove_keyword(answer.text, remove_keyword)
        answer_md5 = qazse.text.md5_str(answer)
        answers_list.append({
            'content': answer,
            'md5': answer_md5
        })
    return {
        "question_title": question_title,
        "question_content": question_content,
        "question_md5": question_md5,
        "answers": answers_list,
        "answer_count": len(answers_list),
        "url": url,
        "type": type,
    }


