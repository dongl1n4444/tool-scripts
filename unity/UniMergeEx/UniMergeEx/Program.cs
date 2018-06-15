using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace UniMergeEx
{
	static class Program
	{
		private static Form1 s_form;

		/// <summary>
		/// 应用程序的主入口点。
		/// </summary>
		[STAThread]
		static void Main(string[] args)
		{
			string s1 = args[0].Trim();
			string s2 = args[1].Trim();
			string s3 = args[2].Trim();
			string s4 = args[3].Trim();

			// for test
			//string s1 = @"C:\Users\ZHUXUD~1\AppData\Local\Temp\p4v\REDA029_redaserver_1666\depot_NBA\branches\pvp\nba_pvp\client\Assets\Scripts\PVP\PvpManager#26(BASE)[0].cs";
			//string s2 = @"C:\Users\ZHUXUD~1\AppData\Local\Temp\t13620t3805.tmp(THEIR)[0].cs";
			//string s3 = @"D:\p4v\depot_NBA\branches\pvp\nba_pvp\client\Assets\Scripts\PVP\PvpManager.cs";
			//string s4 = @"C:\Users\ZHUXUD~1\AppData\Local\Temp\t13620t3805.tmp(MERGE)[0].cs";

			Application.EnableVisualStyles();
			Application.SetCompatibleTextRenderingDefault(false);

			s_form = new Form1();

			try
			{
				Output("Info > arg0 - " + s1);
				Output("Info > arg1 - " + s2);
				Output("Info > arg2 - " + s3);
				Output("Info > arg3 - " + s4);

				string assets_path = s3.Substring(0, s3.IndexOf("\\Assets") + "\\Assets".Length);
				string tmp_folder = assets_path + "\\_unimerge_tmp";

				if (Directory.Exists(tmp_folder) == false)
				{
					Output("Info > create folder - " + tmp_folder);
					Directory.CreateDirectory(tmp_folder);
				}

				var target_file = tmp_folder + "\\" + Path.GetFileNameWithoutExtension(s3) + "_THEIR" + Path.GetExtension(s3);
				SafeCopyFile(s2, target_file);
				Output("Info > copy file - " + s2 + " to " + target_file);
			}
			catch (Exception e)
			{
				Output("Error > " + e.ToString());
			}

			Application.Run(s_form);
		}

		static void SafeCopyFile(string source, string target)
		{
			if (File.Exists(target))
				File.Delete(target);
			File.Copy(source, target);
		}

		private static void Output(string text)
		{
			s_form.richTextBox1.AppendText(text + Environment.NewLine);
		}
	}
}
