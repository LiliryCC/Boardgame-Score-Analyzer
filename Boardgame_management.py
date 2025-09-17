# -*- coding: utf-8 -*-
"""
Created on Sun Sep  7 14:33:11 2025

@author: 35908
"""

import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

class GameScoreSystem:
    def __init__(self):
        # 数据文件
        self.players_file = "players.csv"
        self.games_file = "games.csv"
        
        # 初始化数据
        self.players = self.load_players()
        self.games = self.load_games()
        
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("桌游积分管理系统")
        self.root.geometry("1000x700")  # 增加窗口大小以适应新选项卡
        
        # 创建界面
        self.create_gui()
        
    def load_players(self):
        """加载玩家数据"""
        players = []
        if os.path.exists(self.players_file):
            with open(self.players_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    players.append(row)
        return players
    
    def save_players(self):
        """保存玩家数据"""
        with open(self.players_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['id', 'name']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for player in self.players:
                player_data = {'id': player['id'], 'name': player['name']}
                writer.writerow(player_data)
    
    def load_games(self):
        """加载游戏数据"""
        games = []
        if os.path.exists(self.games_file):
            try:
                # 首先尝试UTF-8编码
                with open(self.games_file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # 将分数从字符串转换为字典
                        scores = eval(row['scores'])
                        row['scores'] = scores
                        # 确保player_count是整数
                        row['player_count'] = int(row['player_count'])
                        games.append(row)
            except UnicodeDecodeError:
                try:
                    # 如果UTF-8失败，尝试GBK编码（常见于中文Windows系统）
                    with open(self.games_file, 'r', newline='', encoding='gbk') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            # 将分数从字符串转换为字典
                            scores = eval(row['scores'])
                            row['scores'] = scores
                            # 确保player_count是整数
                            row['player_count'] = int(row['player_count'])
                            games.append(row)
                except UnicodeDecodeError:
                    # 如果两种编码都失败，尝试使用errors='ignore'忽略错误字符
                    with open(self.games_file, 'r', newline='', encoding='utf-8', errors='ignore') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            # 将分数从字符串转换为字典
                            scores = eval(row['scores'])
                            row['scores'] = scores
                            # 确保player_count是整数
                            row['player_count'] = int(row['player_count'])
                            games.append(row)
            except Exception as e:
                messagebox.showerror("错误", f"加载游戏数据时出错: {str(e)}")
        return games
    
    def save_games(self):
        """保存游戏数据"""
        with open(self.games_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['date', 'player_count', 'scores', 'winner']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for game in self.games:
                # 创建副本以避免修改原始数据
                game_copy = game.copy()
                game_copy['scores'] = str(game['scores'])  # 将字典转换为字符串
                writer.writerow(game_copy)
    
    def create_gui(self):
        """创建图形用户界面"""
        # 创建选项卡
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 玩家管理选项卡
        self.player_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.player_frame, text="玩家管理")
        self.create_player_tab()
        
        # 游戏记录选项卡
        self.record_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.record_frame, text="游戏记录")
        self.create_record_tab()
        
        # 数据分析选项卡
        self.analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.analysis_frame, text="数据分析")
        self.create_analysis_tab()
        
        # 排行榜选项卡
        self.ranking_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.ranking_frame, text="排行榜")
        self.create_ranking_tab()
    
    def create_player_tab(self):
        """创建玩家管理选项卡"""
        # 添加玩家区域
        add_frame = ttk.LabelFrame(self.player_frame, text="添加新玩家")
        add_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(add_frame, text="玩家名称:").grid(row=0, column=0, padx=5, pady=5)
        self.player_name_var = tk.StringVar()
        self.player_name_entry = ttk.Entry(add_frame, textvariable=self.player_name_var)
        self.player_name_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(add_frame, text="添加", command=self.add_player).grid(row=0, column=2, padx=5, pady=5)
        
        # 玩家列表
        list_frame = ttk.LabelFrame(self.player_frame, text="玩家列表")
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 创建树形视图
        columns = ('id', 'name')
        self.player_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        self.player_tree.heading('id', text='ID')
        self.player_tree.heading('name', text='玩家名称')
        
        self.player_tree.column('id', width=50, anchor='center')
        self.player_tree.column('name', width=200, anchor='center')
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.player_tree.yview)
        self.player_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.player_tree.pack(fill='both', expand=True)
        
        # 删除按钮
        ttk.Button(self.player_frame, text="删除选中玩家", command=self.delete_player).pack(pady=5)
        
        # 加载玩家数据
        self.refresh_player_list()
    
    def create_record_tab(self):
        """创建游戏记录选项卡"""
        # 游戏信息区域
        info_frame = ttk.LabelFrame(self.record_frame, text="游戏信息")
        info_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(info_frame, text="玩家人数:").grid(row=0, column=0, padx=5, pady=5)
        self.player_count_var = tk.IntVar(value=3)
        player_count_spin = ttk.Spinbox(info_frame, from_=3, to=7, textvariable=self.player_count_var, 
                                       command=self.update_player_selection)
        player_count_spin.grid(row=0, column=1, padx=5, pady=5)
        
        # 玩家选择区域
        self.player_select_frame = ttk.LabelFrame(self.record_frame, text="选择玩家和输入分数")
        self.player_select_frame.pack(fill='x', padx=10, pady=5)
        
        # 初始化玩家选择
        self.update_player_selection()
        
        # 按钮区域
        button_frame = ttk.Frame(self.record_frame)
        button_frame.pack(pady=5)
        
        ttk.Button(button_frame, text="保存记录", command=self.save_record).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清空输入", command=self.clear_input).pack(side=tk.LEFT, padx=5)
        
        # 历史记录区域
        history_frame = ttk.LabelFrame(self.record_frame, text="历史记录")
        history_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 创建树形视图
        columns = ('date', 'player_count', 'players', 'scores', 'winner')
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show='headings')
        self.history_tree.heading('date', text='游戏日期')
        self.history_tree.heading('player_count', text='玩家人数')
        self.history_tree.heading('players', text='玩家')
        self.history_tree.heading('scores', text='分数')
        self.history_tree.heading('winner', text='胜者')
           
        self.history_tree.column('date', width=50, anchor='center')
        self.history_tree.column('player_count', width=30, anchor='center')
        self.history_tree.column('players', width=150, anchor='center')
        self.history_tree.column('scores', width=100, anchor='center')
        self.history_tree.column('winner', width=50, anchor='center')
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_tree.pack(fill='both', expand=True)
        
        # 加载历史记录
        self.refresh_history()
    
    def create_analysis_tab(self):
        """创建数据分析选项卡"""
        # 选择玩家区域
        select_frame = ttk.LabelFrame(self.analysis_frame, text="选择玩家")
        select_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(select_frame, text="玩家:").grid(row=0, column=0, padx=5, pady=5)
        self.analysis_player_var = tk.StringVar()
        self.analysis_player_combo = ttk.Combobox(select_frame, textvariable=self.analysis_player_var, state="readonly")
        self.analysis_player_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(select_frame, text="生成报告", command=self.generate_report).grid(row=0, column=2, padx=5, pady=5)
        
        # 数据展示区域
        self.analysis_text = tk.Text(self.analysis_frame, wrap=tk.WORD)
        self.analysis_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 加载玩家数据到下拉框
        self.refresh_analysis_players()
    
    def create_ranking_tab(self):
        """创建排行榜选项卡"""
        # 创建主框架
        main_frame = ttk.Frame(self.ranking_frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        
        # 排行榜说明
        desc_frame = ttk.LabelFrame(main_frame, text="排行榜说明")
        desc_frame.pack(fill='x', pady=(0,10))
        
        desc_text = tk.Text(desc_frame, height=4, wrap=tk.WORD)
        desc_text.pack(fill='x', padx=5, pady=5)
        desc_text.insert(tk.END, '''【Rating】基准值为1，是衡量玩家获胜频率的数值
计算方法为: 玩家在有n个人的局中获胜的次数乘以n，将所有n遍历后再除以玩家参加的总局数。
【平均排名百分比】体现的是玩家参与的所有游戏的平均排名
计算方法是玩家在所有游戏中的排名百分比平均值(设100%为第一名，0%为最后一名)。''')
        desc_text.config(state=tk.DISABLED)  # 设置为只读
        
        # 刷新按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=5)
        
        ttk.Button(button_frame, text="刷新排行榜", command=self.refresh_ranking).pack(side=tk.LEFT, padx=5)
        
        # 创建左右两个框架来并排显示两个排行榜
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(side=tk.LEFT, fill='both', expand=True, pady=5)
        
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill='both', expand=True, padx=(0, 5))
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill='both', expand=True, padx=(5, 0))
        
        # 评分排行榜
        rating_frame = ttk.LabelFrame(left_frame, text="RT排行榜")
        rating_frame.pack(fill='both', expand=True)
        
        # 创建树形视图
        columns = ('rank', 'name', 'rating', 'total_games', 'wins')
        self.rating_tree = ttk.Treeview(rating_frame, columns=columns, show='headings')
        self.rating_tree.heading('rank', text='排名')
        self.rating_tree.heading('name', text='玩家名称')
        self.rating_tree.heading('rating', text='RATING')
        self.rating_tree.heading('total_games', text='总局数')
        self.rating_tree.heading('wins', text='获胜局数')
        
        self.rating_tree.column('rank', width=50, anchor='center')
        self.rating_tree.column('name', width=150, anchor='center')
        self.rating_tree.column('rating', width=100, anchor='center')
        self.rating_tree.column('total_games', width=80, anchor='center')
        self.rating_tree.column('wins', width=80, anchor='center')
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(rating_frame, orient=tk.VERTICAL, command=self.rating_tree.yview)
        self.rating_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.rating_tree.pack(fill='both', expand=True)
        
        # 排名百分比排行榜
        rank_percentage_frame = ttk.LabelFrame(right_frame, text="平均排名百分比排行榜")
        rank_percentage_frame.pack(fill='both', expand=True)
        
        # 创建树形视图
        columns2 = ('rank', 'name', 'avg_rank_percentage', 'total_games')
        self.rank_percentage_tree = ttk.Treeview(rank_percentage_frame, columns=columns2, show='headings')
        self.rank_percentage_tree.heading('rank', text='排名', anchor='center')
        self.rank_percentage_tree.heading('name', text='玩家名称', anchor='center')
        self.rank_percentage_tree.heading('avg_rank_percentage', text='平均排名百分比', anchor='center')
        self.rank_percentage_tree.heading('total_games', text='总局数', anchor='center')
        
        # 设置列宽和对齐方式
        self.rank_percentage_tree.column('rank', width=50, anchor='center')
        self.rank_percentage_tree.column('name', width=150, anchor='center')
        self.rank_percentage_tree.column('avg_rank_percentage', width=120, anchor='center')
        self.rank_percentage_tree.column('total_games', width=80, anchor='center')
        
        # 添加滚动条
        scrollbar2 = ttk.Scrollbar(rank_percentage_frame, orient=tk.VERTICAL, command=self.rank_percentage_tree.yview)
        self.rank_percentage_tree.configure(yscroll=scrollbar2.set)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        self.rank_percentage_tree.pack(fill='both', expand=True)
                

                
        # 初始加载排行榜
        self.refresh_ranking()
        
    def calculate_avg_rank_percentage(self, player_name):
        """计算玩家的平均排名百分比"""
        player_games = []
        for game in self.games:
            if player_name in game['scores']:
                player_games.append(game)
        
        if not player_games:
            return 0, 0
        
        rank_percentages = []
        for game in player_games:
            player_count = int(game['player_count'])
            player_score = game['scores'][player_name]
            
            # 获取该游戏中所有分数
            game_scores = list(game['scores'].values())
            # 计算排名百分比
            sorted_scores = sorted(game_scores, reverse=True)
            rank = sorted_scores.index(player_score) + 1
            rank_percentage = (player_count - rank) / (player_count - 1) * 100 if player_count > 1 else 100
            rank_percentages.append(rank_percentage)
        
        avg_rank_percentage = sum(rank_percentages) / len(rank_percentages) if rank_percentages else 0
        return avg_rank_percentage, len(player_games)
    
    def refresh_ranking(self):
        """刷新所有排行榜"""
        # 刷新评分排行榜
        self.rating_tree.delete(*self.rating_tree.get_children())
        
        # 计算所有玩家的rating
        player_ratings = []
        for player in self.players:
            rating, total_games, wins = self.calculate_rating(player['name'])
            player_ratings.append({
                'name': player['name'],
                'rating': rating,
                'total_games': total_games,
                'wins': wins
            })
        
        # 按rating排序
        player_ratings.sort(key=lambda x: x['rating'], reverse=True)
        
        # 添加到评分排行榜
        for i, player_data in enumerate(player_ratings, 1):
            self.rating_tree.insert("", "end", values=(
                i,
                player_data['name'],
                f"{player_data['rating']:.2f}",
                player_data['total_games'],
                player_data['wins']
            ))
        
        # 刷新排名百分比排行榜
        self.rank_percentage_tree.delete(*self.rank_percentage_tree.get_children())
        
        # 计算所有玩家的平均排名百分比
        player_rank_percentages = []
        for player in self.players:
            avg_rank_percentage, total_games = self.calculate_avg_rank_percentage(player['name'])
            player_rank_percentages.append({
                'name': player['name'],
                'avg_rank_percentage': avg_rank_percentage,
                'total_games': total_games
            })
        
        # 按平均排名百分比排序
        player_rank_percentages.sort(key=lambda x: x['avg_rank_percentage'], reverse=True)
        
        # 添加到排名百分比排行榜
        for i, player_data in enumerate(player_rank_percentages, 1):
            self.rank_percentage_tree.insert("", "end", values=(
                i,
                player_data['name'],
                f"{player_data['avg_rank_percentage']:.2f}%",
                player_data['total_games']
            ))

    def calculate_rating(self, player_name):
        """计算玩家的rating"""
        # 初始化各人数游戏的获胜次数
        wins_by_player_count = {3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
        total_games = 0
        
        # 遍历所有游戏记录
        for game in self.games:
            # 检查玩家是否参加了这场游戏
            if player_name in game['scores']:
                total_games += 1
                
                # 检查玩家是否获胜
                if game['winner'] == player_name:
                    player_count = int(game['player_count'])
                    wins_by_player_count[player_count] += 1
        # 计算rating
        weighted_wins = 0
        for player_count, wins in wins_by_player_count.items():
            weighted_wins += wins * player_count

        # 避免除以零
        if total_games == 0:
            return 0, total_games, sum(wins_by_player_count.values())
        rating = weighted_wins / total_games
        return rating, total_games, sum(wins_by_player_count.values())
    
    def refresh_player_list(self):
        """刷新玩家列表"""
        self.player_tree.delete(*self.player_tree.get_children())
        for player in self.players:
            self.player_tree.insert("", "end", values=(player['id'], player['name']))
    
    def refresh_history(self):
        """刷新历史记录"""
        self.history_tree.delete(*self.history_tree.get_children())
        for game in reversed(self.games):
            players = ", ".join(game['scores'].keys())
            scores = ", ".join([str(score) for score in game['scores'].values()])
            self.history_tree.insert( "", "end", values=(game['date'], game['player_count'], players, scores, game['winner']) )
    
    def refresh_analysis_players(self):
        """刷新分析选项卡中的玩家列表"""
        player_names = [player['name'] for player in self.players]
        self.analysis_player_combo['values'] = player_names
        if player_names:
            self.analysis_player_var.set(player_names[0])
    
    def validate_score(self, score_var):
        """验证分数是否在合理范围内"""
        score = score_var.get()
        if score < 10 or score > 100:
            response = messagebox.askyesno(
                "分数验证", 
                f"分数 {score} 不在常见范围内(10-100)。\n您确定要使用这个分数吗？",
                icon=messagebox.WARNING
            )
            if not response:
                # 如果不确定，重置为0
                score_var.set(0)
    
    def update_player_selection(self):
        """更新玩家选择区域"""
        # 清除现有组件
        for widget in self.player_select_frame.winfo_children():
            widget.destroy()
        
        player_count = self.player_count_var.get()
        
        self.player_vars = []
        self.score_vars = []
        
        # 获取所有玩家名称
        player_names = [player['name'] for player in self.players]
        
        for i in range(player_count):
            ttk.Label(self.player_select_frame, text=f"玩家 {i+1}:").grid(row=i, column=0, padx=5, pady=2)
            
            player_var = tk.StringVar()
            player_combo = ttk.Combobox(self.player_select_frame, textvariable=player_var, values=player_names, state="readonly")
            player_combo.grid(row=i, column=1, padx=5, pady=2)
            self.player_vars.append(player_var)
            
            ttk.Label(self.player_select_frame, text="分数:").grid(row=i, column=2, padx=5, pady=2)
            
            score_var = tk.IntVar(value=0)
            # 添加分数验证
            score_spin = ttk.Spinbox(
                self.player_select_frame, 
                from_=0, 
                to=1000, 
                textvariable=score_var, 
                width=10,
                command=lambda var=score_var: self.validate_score(var)
            )
            score_spin.grid(row=i, column=3, padx=5, pady=2)
            # 绑定焦点离开事件
            score_spin.bind("<FocusOut>", lambda event, var=score_var: self.validate_score(var))
            self.score_vars.append(score_var)
    
    def add_player(self):
        """添加新玩家"""
        name = self.player_name_var.get().strip()
        if not name:
            messagebox.showerror("错误", "玩家名称不能为空")
            return
        
        # 检查名称长度
        if len(name) > 20:
            messagebox.showerror("错误", "玩家名称不能超过20个字符")
            return
        
        # 检查是否已存在
        for player in self.players:
            if player['name'].lower() == name.lower():
                messagebox.showerror("错误", f"玩家 {name} 已存在")
                return
        
        # ID生成
        try:
            # 尝试获取现有ID的最大值
            existing_ids = [int(p['id']) for p in self.players if p['id'].isdigit()]
            new_id = max(existing_ids, default=0) + 1
        except (ValueError, KeyError):
            # 如果出现错误，从1开始
            new_id = 1
        
        # 添加新玩家
        new_player = {
            'id': str(new_id),
            'name': name
        }
        
        self.players.append(new_player)
        self.save_players()
        self.player_name_var.set("")
        messagebox.showinfo("成功", f"玩家 {name} 添加成功")
        self.refresh_player_list()
        self.update_player_selection()
        self.refresh_analysis_players()
        
        # 自动聚焦到输入框，方便继续添加
        if hasattr(self, 'player_name_entry'):
            self.player_name_entry.focus_set()
    
    def delete_player(self):
        """删除选中玩家"""
        selected = self.player_tree.selection()
        if not selected:
            messagebox.showerror("错误", "请先选择要删除的玩家")
            return
        
        # 获取选中玩家的ID和名称
        item = self.player_tree.item(selected[0])
        player_id = item['values'][0]
        player_name = item['values'][1]
        
        if messagebox.askyesno("确认", f"确定要删除玩家 {player_name} 吗？"):
            # 删除玩家
            self.players = [p for p in self.players if p['id'] != player_id]
            
            # 更新游戏记录，移除该玩家的分数
            for game in self.games:
                if player_name in game['scores']:
                    del game['scores'][player_name]
                    # 如果胜者是该玩家，需要重新计算胜者
                    if game['winner'] == player_name:
                        if game['scores']:
                            game['winner'] = max(game['scores'].items(), key=lambda x: x[1])[0]
                        else:
                            game['winner'] = "无"
            
            self.save_players()
            self.save_games()
            messagebox.showinfo("成功", f"玩家 {player_name} 已删除")
            
            # 刷新所有相关界面
            self.refresh_player_list()
            self.update_player_selection()
            self.refresh_history()
            self.refresh_analysis_players()
            self.refresh_ranking()
    
    def save_record(self):
        """保存游戏记录"""
        # 验证输入
        players = []
        scores = []
        
        for i, (player_var, score_var) in enumerate(zip(self.player_vars, self.score_vars)):
            player = player_var.get().strip()
            score = score_var.get()
            
            if not player:
                messagebox.showerror("错误", f"请选择玩家 {i+1}")
                return
            
            if player in players:
                messagebox.showerror("错误", f"玩家 {player} 已重复选择")
                return
            
            players.append(player)
            scores.append(score)
        
        # 确定胜者（最高分）
        max_score = max(scores)
        winner_indices = [i for i, score in enumerate(scores) if score == max_score]
        if len(winner_indices) > 1:
            # 有多个赢家，需要选择
            candidate_winners = [players[i] for i in winner_indices]
            winner = self.choose_winner_dialog(candidate_winners)
            if winner is None:
                # 用户取消了选择
                messagebox.showinfo("取消", "保存已取消，请重新选择赢家。")
                return
        else:
            winner = players[winner_indices[0]]
        
        # 创建分数字典
        scores_dict = {}
        for player, score in zip(players, scores):
            scores_dict[player] = score
        
        # 添加游戏记录
        new_game = {
            'date': datetime.now().strftime("%Y-%m-%d"),
            'player_count': len(players),
            'scores': scores_dict,
            'winner': winner
        }
        
        self.games.append(new_game)
        self.save_games()
        messagebox.showinfo("成功", "游戏记录保存成功")
        self.clear_input()
        self.refresh_history()
        self.refresh_ranking()  # 刷新排行榜
        
    def choose_winner_dialog(self, candidate_winners):
        """当有多个玩家获得最高分时，弹出对话框让用户选择赢家"""
        dialog = tk.Toplevel(self.root)
        dialog.title("选择赢家")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示对话框
        dialog.update_idletasks()
        x = (self.root.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (self.root.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 创建说明标签
        label = ttk.Label(dialog, text="有多个玩家获得最高分，请选择赢家:", font=("Arial", 12))
        label.pack(pady=10)
        
        # 选择变量
        selected_player = tk.StringVar()
        
        # 创建选择框架
        select_frame = ttk.Frame(dialog)
        select_frame.pack(fill='x', padx=10, pady=10)
        player_combo = ttk.Combobox(select_frame, textvariable=selected_player, 
                                   values=candidate_winners, state="readonly")
        player_combo.pack(fill='x', padx=5, pady=5)
        player_combo.current(0)  # 默认选择第一个
        
        # 创建按钮框架
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        result = None       
    
        def on_ok():
            nonlocal result
            result = selected_player.get()
            dialog.destroy()
        
        def on_cancel():
            nonlocal result
            result = None
            dialog.destroy()
        
        ttk.Button(button_frame, text="确定", command=on_ok).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=on_cancel).pack(side=tk.RIGHT, padx=5)
            
            # 等待对话框关闭
        self.root.wait_window(dialog)
            
        return result

    def clear_input(self):
        """清空输入"""
        for var in self.player_vars:
            var.set("")
        for var in self.score_vars:
            var.set(0)
    
    def generate_report(self):
        """生成玩家报告"""
        player_name = self.analysis_player_var.get()
        if not player_name:
            messagebox.showerror("错误", "请选择玩家")
            return
        
        # 获取玩家的所有游戏记录
        player_games = []
        for game in self.games:
            if player_name in game['scores']:
                player_games.append(game)
        
        if not player_games:
            self.analysis_text.delete(1.0, tk.END)
            self.analysis_text.insert(tk.END, f"玩家 {player_name} 暂无游戏记录")
            return
        
        # 提取数据
        dates = [game['date'] for game in player_games]
        scores = [game['scores'][player_name] for game in player_games]
        is_winner = [1 if game['winner'] == player_name else 0 for game in player_games]
        player_counts = [game['player_count'] for game in player_games]
        
        # 计算统计信息
        total_games = len(player_games)
        wins = sum(is_winner)
        win_rate = wins / total_games * 100 if total_games > 0 else 0
        avg_score = sum(scores) / total_games if total_games > 0 else 0
        max_score = max(scores) if scores else 0
        min_score = min(scores) if scores else 0
        
        # 计算排名百分比
        rank_percentages = []
        for game in player_games:
            player_count = int(game['player_count'])
            player_score = game['scores'][player_name]
            
            # 获取该游戏中所有分数
            game_scores = list(game['scores'].values())
            # 计算排名百分比
            sorted_scores = sorted(game_scores, reverse=True)
            rank = sorted_scores.index(player_score) + 1
            rank_percentage = (player_count - rank) / (player_count - 1) * 100 if player_count > 1 else 100
            rank_percentages.append(rank_percentage)
        
        avg_rank_percentage = sum(rank_percentages) / len(rank_percentages) if rank_percentages else 0
        
        # 计算rating
        rating, total_games_calc, wins_calc = self.calculate_rating(player_name)
        
        # 显示统计信息
        report_text = f"""
玩家: {player_name}
总游戏场次: {total_games}
获胜场次: {wins}
胜率: {win_rate:.2f}%
平均得分: {avg_score:.2f}
最高得分: {max_score}
最低得分: {min_score}
平均排名百分比(100%为第一名，0%为最后一名): {avg_rank_percentage:.2f}%
评分(Rating): {rating:.2f}

最近5场游戏记录:
"""
        # 添加最近5场游戏记录
        recent_games = player_games[-5:] if len(player_games) > 5 else player_games
        for game in recent_games:
            report_text += f"{game['date']}: 得分 {game['scores'][player_name]}, 排名 {sorted(list(game['scores'].values()), reverse=True).index(game['scores'][player_name]) + 1}/{game['player_count']}, {'获胜' if game['winner'] == player_name else '未获胜'}\n"
        
        # 显示全局统计
        report_text += f"\n全局统计:\n"
        report_text += f"总游戏局数: {len(self.games)}\n"
        
        # 计算最高分和最低分
        all_scores = []
        for game in self.games:
            all_scores.extend(game['scores'].values())
        
        if all_scores:
            report_text += f"全系统最高分: {max(all_scores)}\n"
            report_text += f"全系统最低分: {min(all_scores)}\n"
        
        # 添加图表显示条件
        if total_games < 5:
            report_text += f"\n注意: 由于玩家 {player_name} 只参加了 {total_games} 场游戏，不足5场，因此不显示分析图表。"
        
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, report_text)
        
        # 只在参与场次大于等于5场时才显示图表
        if total_games >= 5:
            # 创建图表
            plt.figure(figsize=(10, 8))
            
            # 分数变化图
            plt.subplot(2, 1, 1)
            # 使用游戏序号而不是日期作为X轴
            game_numbers = list(range(1, total_games + 1))
            plt.plot(game_numbers, scores, 'o-', label='分数')
            plt.title(f'{player_name} 的分数变化')
            plt.xlabel('游戏序号')
            plt.ylabel('分数')
            plt.ylim(min(all_scores) - 1, max(all_scores) + 1)
            plt.grid(True)
            
            # 标记获胜的游戏
            win_games = [i+1 for i in range(total_games) if is_winner[i]]
            win_scores = [scores[i] for i in range(total_games) if is_winner[i]]
            plt.plot(win_games, win_scores, 'ro', label='获胜')
            
            plt.legend()
            
            # 排名百分比图
            plt.subplot(2, 1, 2)
            plt.plot(game_numbers, rank_percentages, 'o-', color='green')
            plt.title(f'{player_name} 的排名百分比变化')
            plt.xlabel('游戏序号')
            plt.ylabel('排名百分比 (%)')
            plt.ylim(-5, 105)
            plt.grid(True)
            plt.axhline(y=avg_rank_percentage, color='r', linestyle='--', label=f'平均: {avg_rank_percentage:.2f}%')
            plt.legend()
            
            plt.tight_layout()
            plt.show()
        else:
            # 如果不足5场，显示提示信息
            messagebox.showinfo("提示", f"玩家 {player_name} 只参加了 {total_games} 场游戏，不足5场，因此不显示分析图表。")
    
    def run(self):
        """运行应用程序"""
        self.root.mainloop()

# 运行应用程序
if __name__ == "__main__":
    app = GameScoreSystem()
    app.run()