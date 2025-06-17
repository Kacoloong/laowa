#include <bits/stdc++.h>
#include "toolkit.h"
using namespace std;
const int ROUND = 25;

signed main() {
    try {
        GRBEnv env = GRBEnv();
        env.set(GRB_IntParam_Threads, 15);
        env.set(GRB_IntParam_OutputFlag, false);
        env.start();
        ofstream fout;
        for (int r = 1; r <= ROUND; r ++) {
//            GRBModel model = GRBModel(env);
//            Algo::makeModel(model, r);
//            model.optimize();
//            cout << r << " " << model.getObjective().getValue() << endl;
            for (int pos1 = 0; pos1 < 128; pos1 ++) {
                for (int pos2 = 0; pos2 < 128; pos2 ++) {
                    GRBModel model = GRBModel(env);
                    Algo::makeModel(model, r, pos1, pos2);
                    cout << "Starting to find round " << r << " with (" << pos1 << ", " << pos2 << ");\n";
                    model.optimize();
                    if (model.get(GRB_IntAttr_Status) == GRB_INFEASIBLE) {
                        fout.open("../impossibleDifferential.txt", ios::app);
                        cout << r << " " << "(" << pos1 << ", " << pos2 << ");\n";
                        fout << r << " " << "(" << pos1 << ", " << pos2 << ");\n";
                        fout.close();
                        goto out;
                    }
                }
            }
            fout.open("../impossibleDifferential.txt", ios::app);
            cout <<"Cannot Find impossible differential of round " << r << ";\n";
            fout <<"Cannot Find impossible differential of round " << r << ";\n";
            fout.close();
        	break;  // 找不到就 break 结束了
		    out:;
        }
    } catch(GRBException e) {
        cout << "Error Code: " << e.getErrorCode() << endl;
        cout << "Error Message: " << e.getMessage() << endl;
    }
}
